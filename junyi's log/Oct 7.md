The default setting for DataLoader is `num_workers=0`, which means that the data loading is synchronous and done in the main process. As a result the main training process has to **wait for the data to be available** to continue the execution.


Setting `num_workers > `0 enables **asynchronous** data loading and **overlap between the training and data loading**. num_workers should be tuned depending on the workload, CPU, GPU, and location of training data.

