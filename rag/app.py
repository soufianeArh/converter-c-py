import gradio as gr
from implementations.question import answer_question
##import the module of question
#add question ingradiop

def main():
      with gr.Blocks() as demo:
            chat=gr.ChatInterface(fn=answer_question, title="Rag QA")
      demo.launch()

if __name__ == "__main__":
      main()