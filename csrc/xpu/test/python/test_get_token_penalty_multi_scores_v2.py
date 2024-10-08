# Copyright (c) 2024 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import paddle
from paddlenlp_ops import get_token_penalty_multi_scores_v2
import unittest

paddle.seed(2023)
class GetTokenPenaltyMultiScoresV2Test(unittest.TestCase):
    def test_get_token_penalty_multi_scores_v2(self):
        pre_ids = paddle.to_tensor([[1, 9, 3, 4, 5, 6, 7, -1, -1, -1], [1, 9, 7, 6, 5, 4, -1, -1, -1, -1]], "int64")
        logits = paddle.to_tensor([[0.1, 0.9, 0.3, 0.4, 0.5, 0.6, 0.7, 0.1, 0.1, 0.1], [0.1, 0.9, 0.7, 0.6, 0.5, 0.4, 0.1, 0.1, 0.1, 0.1]], "float32")
        penalty_scores = paddle.to_tensor([1.0, 1.0], "float32")
        frequency_scores = paddle.to_tensor([0.1, 0.1], "float32")
        presence_scores = paddle.to_tensor([0.0, 0.0], "float32")
        temperatures = paddle.to_tensor([0.5, 0.25], "float32")
        bad_tokens = paddle.to_tensor([0, 1], "int64")
        cur_len = paddle.to_tensor([7, 6], "int64")
        min_len = paddle.to_tensor([1, 8], "int64")
        eos_token_id = paddle.to_tensor([2, 9], "int64")
        print("logits\n", logits)
        get_token_penalty_multi_scores_v2(
            pre_ids,
            logits,
            penalty_scores,
            frequency_scores,
            presence_scores,
            temperatures,
            bad_tokens,
            cur_len,
            min_len,
            eos_token_id,
        )
        print("pre_ids\n", pre_ids)
        print("logits\n", logits)
        print("penalty_scores\n", penalty_scores)
        print("frequency_scores\n", frequency_scores)
        print("presence_scores\n", presence_scores)
        print("temperatures\n", temperatures)
        print("bad_tokens\n", bad_tokens)
        print("cur_len\n", cur_len)
        print("min_len\n", min_len)
        print("eos_token_id\n", eos_token_id)

        ref_logits = np.array(
            [
                [
                    -10000000000,
                    -10000000000,
                    0.6,
                    0.6,
                    0.8,
                    1,
                    1.2,
                    0,
                    0.2,
                    0,
                ],
                [
                    -10000000000,
                    -10000000000,
                    -40000000000,
                    2.4,
                    1.6,
                    1.2,
                    0,
                    0,
                    0.4,
                    -40000000000,
                ],
            ],
            "float32",
        )
        diff_logits = np.sum(np.abs(ref_logits - logits.numpy()))
        print("diff_logits\n", diff_logits)
        assert diff_logits < 1e-6, 'Check failed.'
            
        pre_ids = paddle.to_tensor([[2, 3, 3, 5, 8, 9, 3, 9, 1, 8, 9, 2, 3, 8, 8, 9, 9, 1, 4, 2, 6, 2, 6, 8,
                7, 2, 2, 3, 8, 1, 5, 7, 9, 2, 2, 9, 1, 4, 9, 8, 5, 8, 5, 7, 3, 6, 4, 4,
                9, 9, 8, 5, 5, 2, 2, 9, 4, 8, 1, 9, 6, 9, 2, 2, 7, 2, 2, 9, 4, 6, 4, 6,
                1, 4, 1, 9, 1, 8, 8, 5, 7, 9, 4, 2, 5, 1, 1, 4, 1, 5, 5, 4, 4, 2, 1, 8,
                7, 1, 2, 9, 6, 7, 9, 6, 7, 7, 4, 9, 9, 7, 5, 1, 8, 9, 8, 8, 5, 4, 6, 4,
                7, 5, 5, 7, 6, 9, 3, 9],
                [7, 8, 1, 3, 1, 7, 6, 3, 5, 3, 8, 3, 1, 9, 7, 1, 1, 9, 5, 4, 9, 6, 1, 9,
                3, 8, 3, 9, 9, 6, 4, 2, 8, 5, 3, 1, 6, 9, 1, 3, 9, 8, 1, 7, 5, 1, 5, 1,
                8, 7, 4, 5, 9, 8, 7, 4, 7, 3, 6, 4, 6, 6, 5, 5, 2, 9, 9, 5, 8, 8, 4, 8,
                2, 8, 1, 3, 9, 1, 8, 5, 8, 3, 8, 8, 2, 7, 3, 7, 5, 7, 2, 6, 3, 5, 1, 4,
                6, 1, 9, 8, 2, 2, 3, 6, 7, 6, 2, 6, 5, 1, 5, 6, 2, 1, 6, 4, 7, 7, 3, 8,
                5, 1, 9, 1, 2, 8, 6, 8]])
        logits = paddle.to_tensor([[0.16274983, 0.61470598, 0.94366980, 0.82005417, 0.50752640, 0.38316748,
                0.92648441, 0.24050158, 0.05461595, 0.42218581, 0.36270225, 0.15464807,
                0.13614719, 0.67509544, 0.40315166, 0.10671722, 0.24832056, 0.76091218,
                0.11598995, 0.10962527, 0.04688513, 0.81536716, 0.72259802, 0.60476679,
                0.16701800, 0.84160781, 0.79649884, 0.78021604, 0.75329530, 0.98587888,
                0.13421868, 0.16027625, 0.15269397, 0.06228730, 0.73856270, 0.34721911,
                0.73683006, 0.78178608, 0.32068327, 0.79906309, 0.44214272, 0.63330448,
                0.08016958, 0.63367140, 0.19788943, 0.55346787, 0.11142531, 0.90518415,
                0.21236691, 0.81587470, 0.83752930, 0.70979482, 0.35684183, 0.28715104,
                0.87162822, 0.17679396, 0.98725849, 0.76129991, 0.04090235, 0.37181064,
                0.63317049, 0.24689502, 0.21126501, 0.57617670, 0.74346697, 0.40613672,
                0.56907010, 0.68556929, 0.29032683, 0.17866278, 0.35165095, 0.97015840,
                0.70785582, 0.54259878, 0.14712237, 0.90483177, 0.02094105, 0.36411613,
                0.02495066, 0.88874054, 0.88895452, 0.86216462, 0.58062190, 0.95583254,
                0.20553111, 0.29870346, 0.69652933, 0.36861244, 0.85316223, 0.50240189,
                0.17566244, 0.61080140, 0.88203174, 0.98675215, 0.24344546, 0.17213407,
                0.78160852, 0.25165486, 0.48188508, 0.82812423, 0.10199814, 0.90475923,
                0.66907483, 0.71910626, 0.40660757, 0.59460294, 0.70212913, 0.90841550,
                0.00329034, 0.11290466, 0.89654654, 0.69114941, 0.29473618, 0.62027222,
                0.37333879, 0.98911142, 0.46510187, 0.65914583, 0.73022646, 0.12790845,
                0.12817244, 0.43015456, 0.75011456, 0.43562204, 0.48086026, 0.75587070,
                0.98481447, 0.77367836],
                [0.12336024, 0.74152875, 0.09191196, 0.99301219, 0.44764417, 0.01848883,
                0.78326035, 0.99228370, 0.81447607, 0.02627683, 0.51033205, 0.98703283,
                0.15247856, 0.77640921, 0.60799915, 0.87518770, 0.76818430, 0.86542630,
                0.31795895, 0.04829503, 0.85567141, 0.30271924, 0.67515039, 0.59728831,
                0.78710967, 0.75111693, 0.56837374, 0.49085775, 0.91510201, 0.59545547,
                0.99482232, 0.59036905, 0.58267909, 0.28770933, 0.53237396, 0.95318258,
                0.93987304, 0.61142951, 0.26737869, 0.52285451, 0.03479086, 0.61631846,
                0.66777998, 0.15736090, 0.00447258, 0.37035006, 0.15281211, 0.95372260,
                0.25963321, 0.61036694, 0.15020694, 0.19171195, 0.55252832, 0.00391038,
                0.31052542, 0.96495175, 0.42586124, 0.05630261, 0.99728668, 0.01856293,
                0.83201504, 0.10701843, 0.56434178, 0.38009524, 0.51095045, 0.13202040,
                0.07133843, 0.75313550, 0.17111187, 0.80716974, 0.00172165, 0.83906764,
                0.73240769, 0.85843354, 0.11042888, 0.07912333, 0.33689004, 0.22334915,
                0.59059596, 0.52789515, 0.29831955, 0.39515004, 0.55602801, 0.83818001,
                0.05865780, 0.25654668, 0.76624149, 0.35190639, 0.04158346, 0.59157544,
                0.30779791, 0.94609004, 0.10759670, 0.65575141, 0.37828529, 0.29571742,
                0.76361233, 0.72476572, 0.18568406, 0.85430276, 0.02057583, 0.76195669,
                0.65507215, 0.69129735, 0.25084621, 0.75223947, 0.06064088, 0.20287007,
                0.35887691, 0.75043523, 0.47575447, 0.40021798, 0.44464844, 0.67975360,
                0.40443239, 0.71052992, 0.21782248, 0.50568426, 0.89037591, 0.06661721,
                0.28788096, 0.70773387, 0.42428264, 0.80419677, 0.42710736, 0.87317258,
                0.88229448, 0.79217333]])
        # pre_ids = paddle.to_tensor(np.float32(np.random.random([2, 1024])))
        # logits = paddle.to_tensor(np.float32(np.random.random([2, 1024])))
        penalty_scores = paddle.to_tensor([1.0, 1.0], "float32")
        frequency_scores = paddle.to_tensor([0.1, 0.1], "float32")
        presence_scores = paddle.to_tensor([0.0, 0.0], "float32")
        temperatures = paddle.to_tensor([0.5, 0.25], "float32")
        bad_tokens = paddle.to_tensor([0, 1], "int64")
        cur_len = paddle.to_tensor([7, 6], "int64")
        min_len = paddle.to_tensor([1, 8], "int64")
        eos_token_id = paddle.to_tensor([2, 9], "int64")
        print("logits\n", logits)
        get_token_penalty_multi_scores_v2(
            pre_ids,
            logits,
            penalty_scores,
            frequency_scores,
            presence_scores,
            temperatures,
            bad_tokens,
            cur_len,
            min_len,
            eos_token_id,
        )
        print("pre_ids\n", pre_ids)
        print("logits\n", logits)
        print("penalty_scores\n", penalty_scores)
        print("frequency_scores\n", frequency_scores)
        print("presence_scores\n", presence_scores)
        print("temperatures\n", temperatures)
        print("bad_tokens\n", bad_tokens)
        print("cur_len\n", cur_len)
        print("min_len\n", min_len)
        print("eos_token_id\n", eos_token_id)

        ref_logits = np.array(
            [[-10000000000., -10000000000.,  1.88733959  ,  1.64010835  ,
                1.01505280  ,  0.76633495  ,  1.85296881  ,  0.48100317  ,
                0.10923190  ,  0.84437162  ,  0.72540450  ,  0.30929613  ,
                0.27229437  ,  1.35019088  ,  0.80630332  ,  0.21343444  ,
                0.49664113  ,  1.52182436  ,  0.23197991  ,  0.21925054  ,
                0.09377026  ,  1.63073432  ,  1.44519603  ,  1.20953357  ,
                0.33403599  ,  1.68321562  ,  1.59299767  ,  1.56043208  ,
                1.50659060  ,  1.97175777  ,  0.26843736  ,  0.32055250  ,
                0.30538794  ,  0.12457460  ,  1.47712541  ,  0.69443822  ,
                1.47366011  ,  1.56357217  ,  0.64136654  ,  1.59812617  ,
                0.88428545  ,  1.26660895  ,  0.16033916  ,  1.26734281  ,
                0.39577886  ,  1.10693574  ,  0.22285062  ,  1.81036830  ,
                0.42473382  ,  1.63174939  ,  1.67505860  ,  1.41958964  ,
                0.71368366  ,  0.57430208  ,  1.74325645  ,  0.35358793  ,
                1.97451699  ,  1.52259982  ,  0.08180470  ,  0.74362129  ,
                1.26634097  ,  0.49379003  ,  0.42253003  ,  1.15235341  ,
                1.48693395  ,  0.81227344  ,  1.13814020  ,  1.37113857  ,
                0.58065367  ,  0.35732555  ,  0.70330191  ,  1.94031680  ,
                1.41571164  ,  1.08519757  ,  0.29424474  ,  1.80966353  ,
                0.04188210  ,  0.72823226  ,  0.04990132  ,  1.77748108  ,
                1.77790904  ,  1.72432923  ,  1.16124380  ,  1.91166508  ,
                0.41106221  ,  0.59740692  ,  1.39305866  ,  0.73722488  ,
                1.70632446  ,  1.00480378  ,  0.35132489  ,  1.22160280  ,
                1.76406348  ,  1.97350430  ,  0.48689091  ,  0.34426814  ,
                1.56321704  ,  0.50330973  ,  0.96377015  ,  1.65624845  ,
                0.20399629  ,  1.80951846  ,  1.33814967  ,  1.43821251  ,
                0.81321514  ,  1.18920588  ,  1.40425825  ,  1.81683099  ,
                0.00658068  ,  0.22580932  ,  1.79309309  ,  1.38229883  ,
                0.58947235  ,  1.24054444  ,  0.74667758  ,  1.97822285  ,
                0.93020374  ,  1.31829166  ,  1.46045291  ,  0.25581691  ,
                0.25634488  ,  0.86030912  ,  1.50022912  ,  0.87124407  ,
                0.96172053  ,  1.51174140  ,  1.96962893  ,  1.54735672  ],
                [-10000000000., -10000000000., -40000000000.      ,  3.97204876  ,
                1.79057670  ,  0.07395532  ,  3.13304138  ,  3.96913481  ,
                3.25790429  , -40000000000.      ,  2.04132819  ,  3.94813132  ,
                0.60991424  ,  3.10563684  ,  2.43199658  ,  3.50075078  ,
                3.07273722  ,  3.46170521  ,  1.27183580  ,  0.19318011  ,
                3.42268562  ,  1.21087694  ,  2.70060158  ,  2.38915324  ,
                3.14843869  ,  3.00446773  ,  2.27349496  ,  1.96343100  ,
                3.66040802  ,  2.38182187  ,  3.97928929  ,  2.36147618  ,
                2.33071637  ,  1.15083730  ,  2.12949586  ,  3.81273031  ,
                3.75949216  ,  2.44571805  ,  1.06951475  ,  2.09141803  ,
                0.13916343  ,  2.46527386  ,  2.67111993  ,  0.62944359  ,
                0.01789032  ,  1.48140025  ,  0.61124843  ,  3.81489038  ,
                1.03853285  ,  2.44146776  ,  0.60082775  ,  0.76684779  ,
                2.21011329  ,  0.01564152  ,  1.24210167  ,  3.85980701  ,
                1.70344496  ,  0.22521044  ,  3.98914671  ,  0.07425172  ,
                3.32806015  ,  0.42807373  ,  2.25736713  ,  1.52038097  ,
                2.04380178  ,  0.52808160  ,  0.28535372  ,  3.01254201  ,
                0.68444747  ,  3.22867894  ,  0.00688660  ,  3.35627055  ,
                2.92963076  ,  3.43373418  ,  0.44171551  ,  0.31649333  ,
                1.34756017  ,  0.89339662  ,  2.36238384  ,  2.11158061  ,
                1.19327819  ,  1.58060014  ,  2.22411203  ,  3.35272002  ,
                0.23463120  ,  1.02618670  ,  3.06496596  ,  1.40762556  ,
                0.16633384  ,  2.36630177  ,  1.23119164  ,  3.78436017  ,
                0.43038681  ,  2.62300563  ,  1.51314116  ,  1.18286967  ,
                3.05444932  ,  2.89906287  ,  0.74273622  ,  3.41721106  ,
                0.08230332  ,  3.04782677  ,  2.62028861  ,  2.76518941  ,
                1.00338483  ,  3.00895786  ,  0.24256352  ,  0.81148028  ,
                1.43550766  ,  3.00174093  ,  1.90301788  ,  1.60087192  ,
                1.77859378  ,  2.71901441  ,  1.61772954  ,  2.84211969  ,
                0.87128991  ,  2.02273703  ,  3.56150365  ,  0.26646885  ,
                1.15152383  ,  2.83093548  ,  1.69713056  ,  3.21678710  ,
                1.70842946  ,  3.49269032  ,  3.52917790  ,  3.16869330  ]]
            ,
            "float32",
        )
        print(logits.numpy())
        diff_logits = np.sum(np.abs(ref_logits - logits.numpy()))
        print("diff_logits\n", diff_logits)
        # assert diff_logits < 1e-6, 'Check failed.'

if __name__ == '__main__':
    unittest.main()
