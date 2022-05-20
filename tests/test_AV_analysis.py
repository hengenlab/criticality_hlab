import unittest
import numpy as np
import criticality as cr
import os.path as op
import os


class TestAV_analysis(unittest.TestCase):

    expected_df = 0.27683071748385557
    expected_P_burst = 0.469
    expected_P_t = 0.498
    pvalue_a = 0.05

    def test_AV_analysis(self):

        print(os.getcwd())
        if op.exists('/home/runner/work/criticality_hlab/criticality/tests/'):
            os.chdir('/home/runner/work/criticality_hlab/criticality/tests/')

        # load data
        data = np.load('sample_data.npy')
        perc = 0.25
        flag = 2

        # get avalanches
        r = cr.get_avalanches(data, perc=perc, ncells=-1)

        # get av_size and av_duration
        av_size = r['S']
        av_duration = r['T']

        Result = cr.AV_analysis(av_size, av_duration, flag=flag,
                                plot=True,
                                pltname='',
                                saveloc='')
        Result['scaling_relation_plot']
        print(Result)

        test_df = Result['df']
        msg = "DCC check"
        self.assertEqual(self.expected_df,
                         test_df, msg)

        test_P_burst = Result['P_burst']
        msg = "Pvalue burst"
        self.assertGreaterEqual(test_P_burst, self.pvalue_a, msg)

        test_P_t = Result['P_t']
        msg = "Pvalue T"
        self.assertGreaterEqual(test_P_t, self.pvalue_a, msg)
