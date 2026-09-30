from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModel


MODEL_PATH = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--sentence-transformers--all-MiniLM-L6-v2"
    / "snapshots"
    / "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
)


class MiniLMEmbeddingFunction:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(MODEL_PATH),
            local_files_only=True
        )

        self.model = AutoModel.from_pretrained(
            str(MODEL_PATH),
            local_files_only=True
        )

        self.model.eval()

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state

        input_mask_expanded = (
            attention_mask.unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )

        return torch.sum(
            token_embeddings * input_mask_expanded,
            dim=1
        ) / torch.clamp(
            input_mask_expanded.sum(dim=1),
            min=1e-9
        )

    def _embed(self, texts):
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        with torch.no_grad():
            model_output = self.model(**encoded)

        embeddings = self._mean_pooling(
            model_output,
            encoded["attention_mask"]
        )

        embeddings = torch.nn.functional.normalize(
            embeddings,
            p=2,
            dim=1
        )

        return embeddings.cpu().numpy().tolist()

    def __call__(self, input):
        return self._embed(input)