from .src.gemini import ask_gemini, ask_gemini_system, parse_nl_code, analisys_code

def main():
    response = ask_gemini("What is the capital of France?")
    print("Gemini Response:", response)
    print("-----")
    response_fibo = parse_nl_code("Genere un codigo de que basado en la gramatica que del pdf que calcule fibonacci de manera recursiva. Unicamente retorne el codigo, no adicione comentarios adicionales ni explicaciones.")
    print("Parsed NL Code Response: \n", response_fibo)
    print("-----")
    response_system = ask_gemini_system(f"{response_fibo} explique ese codigo y que tan eficiente es. Sea derecho y sin explicaciones adicionales. Retorne el resumen.")
    print("Gemini System Response: \n", response_system)
    print("-----")
    response_analysis = analisys_code("Analise ese codigo y diga  que tan eficiente y si el codigo realmente calcula fibonacci. Retorne el resumen del analisis.", response_fibo)
    print("Code Analysis Response: \n", response_analysis)