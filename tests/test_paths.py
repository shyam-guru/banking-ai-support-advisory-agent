import ast
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

import retrieval
import vector_store


class TestProjectPaths(unittest.TestCase):

    def test_retrieval_index_paths_use_project_root(self):
        self.assertEqual(
            retrieval.INDEX_FILE,
            PROJECT_ROOT / "data" / "faiss_index" / "banking.index",
        )
        self.assertEqual(
            retrieval.CHUNKS_FILE,
            PROJECT_ROOT / "data" / "faiss_index" / "chunks.json",
        )

    def test_vector_store_output_directory_uses_project_root(self):
        self.assertEqual(
            vector_store.INDEX_DIR,
            PROJECT_ROOT / "data" / "faiss_index",
        )

    def test_prompt_comparison_paths_use_project_root_without_importing_model(self):
        source_path = SRC_DIR / "prompt_comparison.py"
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        assignments = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments[target.id] = ast.unparse(node.value)

        self.assertIn("PROJECT_ROOT", assignments)
        self.assertIn("TEST_FILE", assignments)
        self.assertIn("OUTPUT_FILE", assignments)

        self.assertIn('Path(__file__).resolve().parent.parent', assignments["PROJECT_ROOT"])
        self.assertIn("PROJECT_ROOT", assignments["TEST_FILE"])
        self.assertIn("prompt_test_cases.json", assignments["TEST_FILE"])
        self.assertIn("PROJECT_ROOT", assignments["OUTPUT_FILE"])
        self.assertIn("prompt_comparison_results.json", assignments["OUTPUT_FILE"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
