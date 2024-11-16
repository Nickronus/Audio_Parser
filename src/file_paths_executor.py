import os, re

class FilePathsExecutor():
    def execute(folder_path: str, file_patterns: list[str]) -> list[str]:

        filenames = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                for pattern in file_patterns:
                    if re.match(pattern, file):
                        full_path = os.path.join(root, file)
                        filenames.append(full_path)
                        break
        
        print('Files quantity: ', len(filenames))
        return filenames