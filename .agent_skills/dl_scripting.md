# Skill: Deep Learning Scripting & PyTorch 2.0+ Architecture

## 1. High-Performance PyTorch Boilerplate
When generating or editing deep learning scripts, enforce modern PyTorch 2.0+ performance patterns:
1. **Model Compilation**: Utilize `torch.compile(model)` for 20-30% speedups on Ampere (RTX 3000/A100) or Ada Lovelace (RTX 4000/H100) GPUs.
2. **Automatic Mixed Precision (AMP)**: Always wrap training forward passes in `torch.autocast(device_type='cuda', dtype=torch.float16)` (or `torch.bfloat16` for modern hardware) with `torch.cuda.amp.GradScaler()` to halve VRAM usage and double throughput.
3. **DataLoader Optimization**:
   * Set `num_workers=4` (or match physical CPU cores up to 8).
   * Enable `pin_memory=True` when training on GPUs to accelerate host-to-device memory transfers.
   * Use `persistent_workers=True` if `num_workers > 0` to prevent worker re-initialization overhead between epochs.

## 2. Numerical Stability & Training Dynamics
* **Gradient Clipping**: Always apply gradient clipping (`torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`) before optimizer steps, especially in RNNs, Transformers, and GANs.
* **Weight Initialization**: Explicitly initialize custom layers using Kaiming Normal (`nn.init.kaiming_normal_`) for ReLU/GELU architectures or Xavier Normal (`nn.init.xavier_normal_`) for Sigmoid/Tanh activations.
* **Loss Function Stability**: Use numerically stable combined loss functions (e.g., `nn.BCEWithLogitsLoss` over `nn.Sigmoid` + `nn.BCELoss`, or `nn.CrossEntropyLoss` over `nn.LogSoftmax` + `nn.NLLLoss`).

## 3. Logging & Checkpointing
* **Checkpointing**: Save model state dicts with optimizer states and epoch numbers (`{'epoch': epoch, 'model_state_dict': model.state_dict(), 'optimizer_state_dict': opt.state_dict(), 'best_val_loss': best_val_loss}`).
* **Metric Logging**: Integrate structured training logging (TensorBoard, Weights & Biases, or MLflow) logging training loss every $N$ steps and validation metrics at epoch boundaries.
