# Skill: Deep Learning Scripting (PyTorch 2.0+ & TensorFlow/Keras)

## 1. High-Performance PyTorch Boilerplate
When generating or editing PyTorch scripts, enforce modern PyTorch 2.0+ performance patterns:
1. **Model Compilation**: Utilize `torch.compile(model)` for 20-30% speedups on modern GPUs.
2. **Automatic Mixed Precision (AMP)**: Always wrap training forward passes in `torch.autocast(device_type='cuda', dtype=torch.float16)` with `torch.cuda.amp.GradScaler()` to halve VRAM usage.
3. **DataLoader Optimization**: Set `num_workers=4`, `pin_memory=True`, and `persistent_workers=True`.

## 2. High-Performance TensorFlow / Keras 3 Boilerplate
When working with TensorFlow or Keras 3:
1. **XLA Compilation**: Use `@tf.function(jit_compile=True)` for custom training steps to enable XLA graph optimization.
2. **Mixed Precision**: Initialize `keras.mixed_precision.set_global_policy('mixed_float16')` at the very start of the script.
3. **Dataset Prefetching**: Always chain `.cache().prefetch(tf.data.AUTOTUNE)` to the end of `tf.data.Dataset` pipelines to prevent GPU starvation.

## 3. Numerical Stability & Training Dynamics
* **Gradient Clipping**: Apply gradient clipping (`clip_grad_norm_` in PT, or `clipnorm=1.0` in Keras optimizers) especially for RNNs/Transformers.
* **Loss Function Stability**: Use stable combined loss functions (e.g., `nn.BCEWithLogitsLoss` in PT, or `from_logits=True` in Keras `BinaryCrossentropy`).

## 4. Logging & Checkpointing
* **Checkpointing**: Save full states (model + optimizer + epoch). In Keras, use `ModelCheckpoint(save_weights_only=False)`.
* **Metric Logging**: Integrate TensorBoard/W&B logging metrics at epoch boundaries.
