"""Train the FraudCNN on labeled 8x8 sequence images (X: N x 1 x 8 x 8, y: N)."""
import torch, torch.nn as nn
from processor.processor import FraudCNN  # run from repo root with deps installed

def train(X, y, epochs=20):
    m, opt, loss = FraudCNN(), None, nn.BCELoss()
    opt = torch.optim.Adam(m.parameters(), 1e-3)
    for _ in range(epochs):
        opt.zero_grad(); l = loss(m(X).squeeze(1), y); l.backward(); opt.step()
    torch.save(m.state_dict(), "models/fraud_cnn.pt"); return m
