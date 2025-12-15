#get the vector object
#QUESTIO

from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document

from dotenv import load_dotenv


load_dotenv(override=True)


MODEL = "gpt-4.1-nano"
DB_NAME = str(Path(__file__).parent.parent / "vector_db")

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
RETRIEVAL_K = 10

SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:{context}

"""



vectorestore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)

retriver = vectorestore.as_retriever()
llm = ChatOpenAI(temperature=0, model=MODEL)

# fettch chunks based on all user Question
def retrieveChunks (questions: str):
     return retriver.invoke(questions, k=RETRIEVAL_K)

# get all user questions from history
def userAllMesages (question:str, history:list[dict]):
     print(history)
     #make the user messages in one sitring to get better chunks
     historyUserQuestions="\n".join( m["content"][0]['text'] for m in history if m["role"] == "user")
     allUserQuestions = historyUserQuestions + '\n' + question
     return allUserQuestions

# callback function or inference function.
# its responsible
def answer_question(question: str, history: list[dict]=[]):
      allUserMessages = userAllMesages(question, history) # "who is every" and then "what she did before"
      retrievedChuncks = retrieveChunks(allUserMessages)
      context="\n\n".join(doc.page_content for doc in retrievedChuncks)
      SYSTEM_PROMPT=SYSTEM_PROMPT_TEMPLATE.format(context=context)
      messages = [
         SystemMessage(content=SYSTEM_PROMPT),
      ]
      messages.extend(convert_to_messages(history))
      messages.append(HumanMessage(content=question))

      response = llm.invoke(messages)
      return response.content


if __name__ == "__main__":
    test=answer_question("who is avery")
    print(test)



