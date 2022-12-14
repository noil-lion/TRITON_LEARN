import numpy as np
import threading

import tritonclient.grpc as grpcclient


def client_init(url="localhost:40184",
                ssl=False, private_key=None, root_certificates=None, certificate_chain=None,
                verbose=False):
    """
    :param url:
    :param ssl: Enable SSL encrypted channel to the server
    :param private_key: File holding PEM-encoded private key
    :param root_certificates: File holding PEM-encoded root certificates
    :param certificate_chain: File holding PEM-encoded certicate chain
    :param verbose:
    :return:
    """
    triton_client = grpcclient.InferenceServerClient(
        url=url,
        verbose=verbose,
        ssl=ssl,
        root_certificates=root_certificates,
        private_key=private_key,
        certificate_chain=certificate_chain)

    return triton_client


def infer(triton_client, model_name,
          input0='INPUT__0',output0='OUTPUT__0', 
          compression_algorithm=None):
    inputs = []
    outputs = []
    # batch_size=8
    # 如果batch_size超过配置文件的max_batch_size，infer则会报错
    # INPUT0、INPUT1为配置文件中的输入节点名称
    inputs.append(grpcclient.InferInput(input0, [1, 1, 128, 160, 112], "FP32"))

    # Initialize the data
    # np.random.seed(2022)
    inputs[0].set_data_from_numpy(np.random.random([1, 1, 128, 160, 112]).astype(np.float32))

    # OUTPUT0、OUTPUT1为配置文件中的输出节点名称
    outputs.append(grpcclient.InferRequestedOutput(output0))

    results = triton_client.infer(
        model_name=model_name,
        inputs=inputs,
        outputs=outputs,
        compression_algorithm=compression_algorithm
        # client_timeout=0.1
    )
    # print(results)
    # 转化为numpy格式
    # print(results.as_numpy(output0))




if __name__ == '__main__':
    import time

    client = client_init()



    s = time.time()
    for i in range(0, 100):
        infer(triton_client=client, model_name='airway')
    #
    # infer(triton_client=client, model_name='tf_graphdef')
    #
    # infer(triton_client=client, model_name='torch_model',
    #       input0='INPUT__0', input1='INPUT__1',
    #       output0='OUTPUT__0', output1='OUTPUT__1')
    #
    # infer(triton_client=client, model_name='tf_onnx',
    #       input0='INPUT:0', input1='INPUT:1')

    # infer(triton_client=client, model_name='torch_onnx')

    # infer(triton_client=client, model_name='trt_model')

    print("grpc infer: {}".format(time.time() - s))