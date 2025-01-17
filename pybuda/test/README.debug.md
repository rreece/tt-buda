
*Test specific environment variables that can be used to fine tune default behavior of PyBuda RGG tests.*

## Parameters
 * RANDOM\_TEST\_COUNT: Number of random tests to be generated and executed. The parameter generate test_index in range from 0 to RANDOM\_TEST\_COUNT-1. (default: 5)
 * RANDOM\_TESTS\_SELECTED: Limiting random tests to only selected subset defined as comma separated list of test indexes. E.x. "3,4,6". Default is no limitation if not specified or empty.
 * MIN\_DIM: Minimal number of dimensions of input tensors. (default: 3)
 * MAX\_DIM: Maximum number of dimensions of input tensors. (default: 4)
 * MIN\_OP\_SIZE\_PER\_DIM: Minimal size of an operator dimension. (default: 16)
 * MAX\_OP\_SIZE\_PER\_DIM: Maximum size of an operator dimension. Smaller operator size results in fewer failed tests. (default: 512)
 * MIN_MICROBATCH_SIZE: Minimal size of microbatch of an input tensor. (default: 1)
 * MAX_MICROBATCH_SIZE: Maximum size of microbatch of an input tensor. (default: 8)
 * NUM\_OF\_NODES\_MIN: Minimal number of nodes to be generated by RGG. (default: 5)
 * NUM\_OF\_NODES\_MAX: Maximum number of nodes to be generated by RGG. (default: 10)
 * NUM\_OF\_FORK\_JOINS\_MAX: Maximum number of fork joins to be generated by random graph algorithm in RGG. (default: 50)
 * CONSTANT\_INPUT\_RATE: Rate of constant inputs in RGG in percents. (default: 50)
 * SAME\_INPUTS\_PERCENT\_LIMIT: Percent limit of nodes which have same value on multiple inputes. (default: 10)
