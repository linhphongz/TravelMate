import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai

load_dotenv()
class Document:
    def __init__(self, metadata, page_content):
        self.metadata = metadata
        self.page_content = page_content
class PDFVectorDatabase:
    def __init__(self, pdf_data_path="C:\\Users\\admin\\Test_private_github\\LLM-RAG\\src\\data_src", 
                 vector_db_path="C:\\Users\\admin\\Test_private_github\\LLM-RAG\\src\\data_src\\vector_index"):
        """
        Initializes the PDFVectorDatabase instance.

        Args:
            pdf_data_path (str): Path to the directory containing PDF documents.
            vector_db_path (str): Path to the directory where the vector index will be stored.

        Raises:
            ValueError: If no documents are found in the specified directory and the vector index does not exist.
        """
        self.documents = []
        self.texts = []
        self.vector_index = None
        self.pdf_data_path = pdf_data_path
        self.vector_db_path = vector_db_path
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))
        
        if not self._check_vector_db_exists():
            self._create_db_from_files()
        else:
            self.vector_index = Chroma(persist_directory=vector_db_path,embedding_function=self.embedding_model)

    def _check_vector_db_exists(self):
        """
        Checks if the vector database already exists.

        Returns:
            bool -> True if the vector database exists and contains files, False otherwise.
        """
        return os.path.exists(self.vector_db_path) and len(os.listdir(self.vector_db_path)) > 0

    def _create_db_from_files(self):
        """
        Creates the vector database from PDF files by loading documents,
        splitting text, and creating a vector index.
        """
        self._load_documents()
        self._split_text()
        self._create_vector_index()

    def _load_documents(self):
        """
        Loads PDF documents from the specified directory.

        Raises:
            ValueError: If no documents are found in the specified directory.
        """
        loader = DirectoryLoader(self.pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
        self.documents = loader.load()
        if not self.documents:
            raise ValueError("No documents found in the specified directory.")

    def _split_text(self):
        """
        Splits the loaded documents into smaller text chunks for indexing.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        self.texts = text_splitter.split_documents(self.documents)

    def _create_vector_index(self):
        """
        Creates a vector index from the split text chunks and persists it.

        Raises:
            ValueError: If no texts are found to create the vector index.
        """
        if not self.texts:
            raise ValueError("No texts found to create vector index.")
        self.vector_index = Chroma.from_documents(self.texts, self.embedding_model, persist_directory=self.vector_db_path)
        self.vector_index.persist()

    def handleListDoc(self,docs):
        output_lines = []
        for doc in docs:
            output_lines.append(doc.page_content)
            output_lines.append("\n")

        final_output = '\n'.join(output_lines)
        return final_output

    def search(self, query, k=3):
        """
        Searches for similar documents based on the provided query.

        Args:
            query (str): The search query.
            k (int): The number of similar documents to return (default is 5).

        Returns:
            list -> A list of documents that are similar to the query.
        """
        if query is None:
            print("E")
            return " "
        similar_docs = self.vector_index.similarity_search(query=query, k=k)
        return self.handleListDoc(similar_docs)

    def _validate_pdf_path(self, pdf_path):
        """
        Validates the specified PDF path.

        Args:
            pdf_path (str): The path to the PDF file.

        Raises:
            FileNotFoundError: If the specified file does not exist or is not a valid PDF.
        """
        if not os.path.isfile(pdf_path) or not pdf_path.endswith('.pdf'):
            raise FileNotFoundError(f"The file {pdf_path} does not exist or is not a valid PDF.")

    def _handle_api_error(self, func, *args, **kwargs):
        """
        Handles API call errors.

        Args:
            func (callable): The function to call.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            any -> The result of the function call or None if an error occurs.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while calling the API: {e}")
            return None