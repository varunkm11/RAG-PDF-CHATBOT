from inngest import Inngest

inngest_client = Inngest(app_id="rag-pdf-chatbot")


@inngest_client.create_function(
    fn_id="process-pdf"
)
def process_pdf(ctx):
    print("PDF Processing Started")