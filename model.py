from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_classic.chains import RetrievalQA
import ollama
from pathlib import Path

# 1. Загрузка документов
# Можно добавить цикл, чтобы прочитать все файлы из папки data_bearings
directory = Path('C:\engineer\data_bearings')
for pdffile in directory.iterdir():
    loader = PyPDFLoader(pdffile)
    documents = loader.load()

# 2. Нарезка текста на куски (чтобы ИИ было проще искать)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 3. Создание векторной базы (локально)
# Используем легкую модель для векторизации
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.from_documents(docs, embeddings)

# 4. Инициализация локальной нейросети (через Ollama)
llm = OllamaLLM(model="llama3")

# 5. Создание цепочки "Вопрос - Поиск в базе - Ответ"
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_db.as_retriever(),
)

# Функция для бота
async def get_bearing_answer(question: str):
    # Добавляем жесткую инструкцию в промпт
    system_prompt = (
        f"Ты — технический эксперт по подшипникам. Отвечай ТОЛЬКО на основе базы знаний. "
        f"Твои ответы должны быть  короткими, но содержащими всю нужную информацию "
        f"Отвечай всегда ТОЛЬКО на русском языке"
        f"Если информации нет или вопрос не про подшипники, ответь: 'Я специализируюсь только на подшипниках'.\n"
        f"Вопрос: {question}"
    )
    # response = qa_chain.invoke(full_query)
    response = ollama.chat(model='llama3:8b', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': question},
    ])
    
    return response['message']['content']
    # return response["result"]
