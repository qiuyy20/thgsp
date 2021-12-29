#include <torch/script.h>
#include "cpu/dsatur_cpu.h"

torch::Tensor dsatur(const torch::Tensor& rowptr, const torch::Tensor& col){
    if (rowptr.device().is_cuda()){
    #ifdef WITH_CUDA
         AT_ERROR("No CUDA version supported");
    #else
         AT_ERROR("Not compiled with CUDA support");
    #endif
    } else{
        return dsatur_coloring_cpu(rowptr,col);
    }
}

static auto registry=torch::RegisterOperators().op("thgsp::dsatur", &dsatur);

