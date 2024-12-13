import os
"""
このスクリプトは、Azure Document Intelligence APIを使用してPDFドキュメントを解析し、特定のキーワードを検索します。
使用方法:
    python sample_poc.py <pdf_path> <search_keyword>
引数:
    pdf_path (str): 解析するPDFドキュメントのパス。
    search_keyword (str): ドキュメント内で検索するキーワード。
環境変数:
    DOCUMENTINTELLIGENCE_ENDPOINT: Azure Document Intelligence APIのエンドポイント。
    DOCUMENTINTELLIGENCE_API_KEY: Azure Document Intelligence APIのキー。
例外処理:
    HttpResponseError: APIリクエストが失敗した場合に発生する例外。エラーメッセージとコードに基づいて詳細な情報を提供します。
関数:
    analyze_with_highres(pdf_path, search_keyword):
        PDFドキュメントを解析し、キーワードを検索します。手書きの内容が含まれているかどうかもチェックします。
"""


def analyze_with_highres(pdf_path, search_keyword):
    path_to_sample_documents = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../..",
            pdf_path,
        )
    )
    # [START analyze_with_highres]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult

    def _in_span(word, spans):
        for span in spans:
            if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
                return True
        return False

    def _format_polygon(polygon):
        if not polygon:
            return "N/A"
        return ", ".join([f"[{polygon[i]}, {polygon[i + 1]}]" for i in range(0, len(polygon), 2)])

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Specify which add-on capabilities to enable.
    with open(path_to_sample_documents, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            features=[DocumentAnalysisFeature.OCR_HIGH_RESOLUTION],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()

    if result.styles and any([style.is_handwritten for style in result.styles]):
        print("Document contains handwritten content")
    else:
        print("Document does not contain handwritten content")

    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")
        print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        if page.lines:
            is_keyword_found = False
            for line_idx, line in enumerate(page.lines):
                words = []
                # if page.words:
                #     for word in page.words:
                #         print(f"......Word '{word.content}' has a confidence of {word.confidence}")
                #         if _in_span(word, line.spans):
                #             words.append(word)
                # print(
                #     f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
                #     f"within bounding polygon '{_format_polygon(line.polygon)}'"
                # )

                if search_keyword in line.content:
                    print(f"Found keyword '{search_keyword}' in line '{line.content}'")
                    is_keyword_found = True
            if not is_keyword_found:
                print(f"Keyword '{search_keyword}' not found in page #{page.page_number}")

        # if page.selection_marks:
        #     for selection_mark in page.selection_marks:
        #         print(
        #             f"Selection mark is '{selection_mark.state}' within bounding polygon "
        #             f"'{_format_polygon(selection_mark.polygon)}' and has a confidence of {selection_mark.confidence}"
        #         )

    if result.tables:
        for table_idx, table in enumerate(result.tables):
            print(f"Table # {table_idx} has {table.row_count} rows and " f"{table.column_count} columns")
            if table.bounding_regions:
                for region in table.bounding_regions:
                    print(
                        f"Table # {table_idx} location on page: {region.page_number} is {_format_polygon(region.polygon)}"
                    )
            for cell in table.cells:
                print(f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'")
                if cell.bounding_regions:
                    for region in cell.bounding_regions:
                        print(
                            f"...content on page {region.page_number} is within bounding polygon '{_format_polygon(region.polygon)}'"
                        )

    print("----------------------------------------")
    # [END analyze_with_highres]


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    import argparse

    parser = argparse.ArgumentParser(description="Analyze formulas in a PDF document.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF document.")
    parser.add_argument("search_keyword", type=str, help="Keyword to search in the document.")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    search_keyword = args.search_keyword

    try:
        load_dotenv(find_dotenv())
        analyze_with_highres(pdf_path, search_keyword)
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
