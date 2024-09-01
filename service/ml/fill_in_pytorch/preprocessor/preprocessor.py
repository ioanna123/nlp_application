import re


class Preprocessor:
    @staticmethod
    def _clean_str(sentence: str) -> str:
        """
        Cleans string from symbols etc

        @param sentence: str sentence
        @return: The cleaned sentence
        """
        return re.sub(r'[^\w\s<>]', '', sentence)

    @staticmethod
    def _create_mask(sentence: str) -> str:
        """
        Replace <blank> with [MASK]
        @param sentence:str sentence
        @return:
        """
        return sentence.replace('<blank>', '[MASK]')

    def transform(self, sentence: str) -> str:
        """
        Transforms the sentence with the correct format
        """
        return self._create_mask(self._clean_str(sentence))
