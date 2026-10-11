import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

MODEL = 'gpt-4o-mini'
db_name = 'personal_vector_db'
NOTION_API_BASE_URL = 'https://api.notion.com'
NOTION_API_RETRIEVE_BLOCK_CHILDREN_ENDPOINT = '/v1/blocks/{block_id}/children'
NOTION_API_RETRIEVE_PAGE_ENDPOINT = '/v1/pages/{page_id}'
NOTION_VERSION = '2022-06-28'
NOTION_2ND_BRAIN_PAGE_ID = 'a69fa94d-ccb2-4445-861f-85ee5b921070'
NOTION_PROJECTS_PAGE_ID = 'f82faa20-e678-47ea-b983-655dd4b12e1a'
NOTION_AREAS_PAGE_ID = '57ca6e21-1a84-4d95-b60e-d0012a34d530'
NOTION_RESOURCES_PAGE_ID = 'c62a47f2-ca73-4a71-b683-288b3a866fda'
NOTION_ARCHIVE_PAGE_ID = '237c2a62-08af-450f-b01a-26e04a3c8781'
RELEVANT_PAGE_IDS = [NOTION_PROJECTS_PAGE_ID, NOTION_AREAS_PAGE_ID, NOTION_RESOURCES_PAGE_ID, NOTION_ARCHIVE_PAGE_ID]

# Load environment variables in a file called .env

load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
notion_api_token = os.getenv('NOTION_TOKEN', 'your-key-if-not-using-env')

headers = {
    'Authorization': f'Bearer {notion_api_token}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

NOTION_TIMEOUT = (5, 30)  # (connect, read) seconds

# Retry rate limits (429, honoring Retry-After) and transient errors with exponential backoff and jitter
notion_retry = Retry(
    total=5,
    backoff_factor=1,
    backoff_jitter=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods={"GET"},
    respect_retry_after_header=True,
    raise_on_status=False,
)
session = requests.Session()
session.headers.update(headers)
session.mount('https://', HTTPAdapter(max_retries=notion_retry))
session.mount('http://', HTTPAdapter(max_retries=notion_retry))

# Blocks and pages skipped because Notion returned an error, reported at the end of the run
skipped: List[Dict[str, Any]] = []

class NotionRequestError(Exception):
    """A Notion request failed with an error status or after exhausting retries."""
    def __init__(self, target_id: str, status: Any, code: str | None = None):
        super().__init__(f"Notion request for {target_id} failed: {status} {code or ''}".strip())
        self.target_id = target_id
        self.status = status
        self.code = code

def notion_get(url: str, target_id: str, params: Dict[str, Any] | None = None) -> Dict[Any, Any]:
    """GET a Notion endpoint and return its JSON, raising NotionRequestError on any failure."""
    try:
        response = session.get(url, params=params, timeout=NOTION_TIMEOUT)
    except requests.exceptions.Timeout:
        raise NotionRequestError(target_id, "timeout")
    except requests.RequestException:
        raise NotionRequestError(target_id, "connection")

    if not response.ok:
        try:
            code = response.json().get("code")
        except ValueError:
            code = None
        raise NotionRequestError(target_id, response.status_code, code)

    return response.json()

def record_skip(error: NotionRequestError, kind: str, block_type: str | None = None) -> None:
    """Remember a skipped block subtree or root page and warn about it (ids and error codes only)."""
    entry = {"kind": kind, "id": error.target_id, "block_type": block_type, "status": error.status, "code": error.code}
    skipped.append(entry)
    print(f"WARNING: skipped {describe_skip(entry)}")

def describe_skip(entry: Dict[str, Any]) -> str:
    block_type = f" ({entry['block_type']})" if entry["block_type"] else ""
    code = f" {entry['code']}" if entry["code"] else ""
    return f"{entry['kind']} {entry['id']}{block_type}: {entry['status']}{code}"

def get_block_children(block_id: str) -> List[Dict[Any, Any]]:
    """Recursively fetch all children blocks of a given block."""
    url = NOTION_API_BASE_URL + NOTION_API_RETRIEVE_BLOCK_CHILDREN_ENDPOINT.format(block_id=block_id)
    data = notion_get(url, block_id)

    results = data["results"]

    # Handle pagination
    while data.get("has_more", False):
        data = notion_get(url, block_id, params={"start_cursor": data["next_cursor"]})
        results.extend(data["results"])

    # Process each block recursively if it has children
    all_blocks = []
    for block in results:
        all_blocks.append(block)

        # Check if the block has children
        if block.get("has_children", False):
            try:
                child_blocks = get_block_children(block["id"])
            except NotionRequestError as error:
                # Keep the block itself, skip only its descendants
                record_skip(error, "block subtree", block_type=block.get("type"))
                continue
            all_blocks.extend(child_blocks)
    
    return all_blocks

def extract_text_from_block(block: Dict[Any, Any]) -> str:
    """Extract text content from a Notion block."""
    block_type = block["type"]
    
    if block_type == "paragraph":
        return extract_rich_text(block["paragraph"]["rich_text"])
    elif block_type == "heading_1":
        return "# " + extract_rich_text(block["heading_1"]["rich_text"])
    elif block_type == "heading_2":
        return "## " + extract_rich_text(block["heading_2"]["rich_text"])
    elif block_type == "heading_3":
        return "### " + extract_rich_text(block["heading_3"]["rich_text"])
    elif block_type == "bulleted_list_item":
        return "• " + extract_rich_text(block["bulleted_list_item"]["rich_text"])
    elif block_type == "numbered_list_item":
        return "1. " + extract_rich_text(block["numbered_list_item"]["rich_text"])
    elif block_type == "to_do":
        checked = "✓ " if block["to_do"]["checked"] else "☐ "
        return checked + extract_rich_text(block["to_do"]["rich_text"])
    elif block_type == "toggle":
        return extract_rich_text(block["toggle"]["rich_text"])
    elif block_type == "code":
        language = block["code"].get("language", "")
        return f"```{language}\n{extract_rich_text(block['code']['rich_text'])}\n```"
    elif block_type == "callout":
        return f"> {extract_rich_text(block['callout']['rich_text'])}"
    elif block_type == "quote":
        return f"> {extract_rich_text(block['quote']['rich_text'])}"
    elif block_type == "divider":
        return "---"
    else:
        return ""

def extract_rich_text(rich_text_list: List[Dict[Any, Any]]) -> str:
    """Extract text from rich_text objects."""
    if not rich_text_list:
        return ""

    return "".join([text_obj.get("plain_text", "") for text_obj in rich_text_list])

def get_page_content(page_id: str) -> Dict[str, Any]:
    """Get all content from a Notion page including its properties and blocks."""
    # Get page properties
    page_url = NOTION_API_BASE_URL + NOTION_API_RETRIEVE_PAGE_ENDPOINT.format(page_id=page_id)
    page_data = notion_get(page_url, page_id)
    
    # Get page title
    title = ""
    for prop_name, prop_value in page_data.get("properties", {}).items():
        if prop_value.get("type") == "title":
            title = extract_rich_text(prop_value.get("title", []))
            break
    
    # Get page blocks
    blocks = get_block_children(page_id)
    
    # Extract text from blocks
    content = []
    for block in blocks:
        text = extract_text_from_block(block)
        if text:
            content.append(text)
    
    return {
        "id": page_id,
        "title": title,
        "content": "\n".join(content),
        "url": f"https://notion.so/{page_id.replace('-', '')}"
    }

def vectorize_notion_notes(page_ids: list[str], collection_name: str = "notion_notes"):
    """
    Fetch all notes from a Notion database, vectorize them and store in Chroma.
    
    Args:
        database_id: The ID of the Notion database containing your notes
        collection_name: Name for your Chroma collection
    """
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()
    
    # Initialize Chroma vector store
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_name
    )
    
    # Text splitter for chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    skipped.clear()

    # Process each page
    for page_id in page_ids:
        print(f"Processing page: {page_id}")

        # Get page content; a failing root is skipped so the other roots still get indexed
        try:
            page_data = get_page_content(page_id)
        except NotionRequestError as error:
            record_skip(error, "root page")
            continue
        
        # Split text into chunks
        chunks = text_splitter.split_text(page_data["content"])
        
        # Create metadata for each chunk
        metadatas = [
            {
                "source": page_data["url"],
                "title": page_data["title"],
                "page_id": page_id
            } for _ in chunks
        ]
        
        # Add documents to the vector store
        if chunks:
            vectordb.add_texts(
                texts=chunks,
                metadatas=metadatas,
                ids=[f"{page_id}-chunk-{i}" for i in range(len(chunks))]
            )
    
    # Report what was skipped because of Notion errors
    if skipped:
        print(f"Skipped {len(skipped)} item(s) because of Notion errors:")
        for entry in skipped:
            print(f"  - {describe_skip(entry)}")
    else:
        print("Nothing skipped.")

    # Chroma persists to persist_directory automatically
    print(f"Vectorization complete! Stored in {db_name}")

    return vectordb

if __name__ == "__main__":
    vectorstore = vectorize_notion_notes(page_ids=RELEVANT_PAGE_IDS)