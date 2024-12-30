import tokenize
from io import StringIO
from typing import Dict
import keyword

class CustomKeywordParser:
    def __init__(self, keyword_mapping: Dict[str, str]):

        self.keyword_mapping = keyword_mapping
        self.reverse_mapping = {v: k for k, v in keyword_mapping.items()}
        self.python_keywords = keyword.kwlist


    def translate_to_python(self, custom_code: str) -> str:
        try:
            buffer = StringIO(custom_code)
            tokens = tokenize.generate_tokens(buffer.readline)

            translated_tokens = []
            token_stack = []
            for token in tokens:
                if token.type == tokenize.STRING:
                    if not token_stack or token_stack[-1] != "STRING":
                        token_stack.append("STRING")
                    else:
                        token_stack.pop()
                elif token.type == tokenize.COMMENT:
                    translated_tokens.append(token)
                    continue
                elif token.exact_type in (tokenize.LPAR, tokenize.LSQB, tokenize.LBRACE):
                    token_stack.append(token.string)
                elif token.exact_type in (tokenize.RPAR, tokenize.RSQB, tokenize.RBRACE):
                    if token_stack:
                        token_stack.pop()

                if not token_stack and token.type == tokenize.NAME and token.string in self.keyword_mapping:
                    translated_token = tokenize.TokenInfo(
                        type=token.type,
                        string=self.keyword_mapping[token.string],
                        start=token.start,
                        end=token.end,
                        line=token.line
                    )
                    translated_tokens.append(translated_token)
                else:
                    translated_tokens.append(token)

            result = []
            prev_row = 1
            prev_col = 0

            for token in translated_tokens:
                row, col = token.start
                if row > prev_row:
                    result.append("\n" * (row - prev_row))
                    prev_col = 0

                if col > prev_col:
                    result.append(" " *  (col - prev_col))

                result.append(token.string)
                prev_row, prev_col = token.end

            return "".join(result)
        except tokenize.TokenError as e:
            raise SyntaxError(f"Invalid syntax in custom code: {str(e)}")
        except Exception as e:
            raise Exception(f"Error translating code: {str(e)}")


