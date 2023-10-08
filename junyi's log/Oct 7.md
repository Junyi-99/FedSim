The default setting for DataLoader is `num_workers=0`, which means that the data loading is synchronous and done in the main process. As a result the main training process has to **wait for the data to be available** to continue the execution.


Setting `num_workers > `0 enables **asynchronous** data loading and **overlap between the training and data loading**. num_workers should be tuned depending on the workload, CPU, GPU, and location of training data.

2、Dataloader(dataset, num_workers=4*num_GPU)
3、Dataloader(dataset, pin_memory=True)

# 数据操作
4、直接在设备中创建torch.Tensor，不要在一个设备中创建再移动到另一个设备中
5、避免CPU和GPU之间不必要的数据传输
6、使用torch.from_numpy(numpy_array)或者torch.as_tensor(others)
7、在数据传输操作可以重叠时，使用tensor.to(non_blocking=True)
8、使用PyTorch JIT将元素操作融合到单个kernel中。

# 训练
10、将batch size设置为8的倍数，最大化GPU内存的使用
11、前向的时候使用混合精度（后向的使用不用）
12、在优化器更新权重之前，设置梯度为None，model.zero_grad(set_to_none=True)
13、梯度积累：每隔x个batch更新一次权重，模拟大batch size的效果

# 推理/验证
14、关闭梯度计算



# overall time
50/775 data loads (cache already generated)
original: 1082.313ms
optimized(vanilla): 1294.531ms
optimized(pinmemory): 1249.816ms
optimized(replace repeat with list): 1225.090ms
time expand: 212.218ms

## tqdm.__iter__
original: wallDuration: 182.303ms, selfTime: 0.731ms, avgDuration: 3.646ms, occurrences: 50
optimized(vanilla): wallDuration: 338.245ms, selfTime: 0.526ms, avgDuration: 6.765ms, occurrences: 50
optimized(pinmemory): wallDuration: 340.467ms, selfTime: 0.708ms, avgDuration: 6.809ms, occurrences: 50
optimized(replace repeat with list): 326.282ms, selfTime: 0.419ms, avgDuration: 6.526ms, occurrences: 50
optimized(): ms, selfTime: ms, avgDuration: ms, occurrences: 50
optimized(): ms, selfTime: ms, avgDuration: ms, occurrences: 50
(time expanded: 155.942ms)

### __getitem__
original: wallDuration: 54.655ms, selfTime: 23.977ms, avgDuration: 0.009ms, occurrences: 6400
optimized(vanilla): wallDuration: 301.570ms, selfTime: 76.189ms, avgDuration: 0.047ms, occurrences: 6400
optimized(pinmemory): wallDuration: 304.400ms, selfTime: 74.203ms, avgDuration: 0.048ms, occurrences: 6400
optimized(replace repeat with list): 293.517ms, selfTime: 77.641ms, avgDuration: 0.046ms, occurrences: 6400
optimized(): ms, selfTime: ms, avgDuration: ms, occurrences: 6400
optimized(): ms, selfTime: ms, avgDuration: ms, occurrences: 6400

(getitem expanded 246.915ms)



