import unittest
import numpy as np
import criticality as cr


class Testtplfit_new(unittest.TestCase):
    '''
    Create synthetic data and test tpfilt_new can find xmin
    '''

    xmin_list = [2, 4, 8, 10, 20, 40]
    xmax_list = [500, 1000, 1000, 1000, 1000, 2000, 3000]
    alpha_list = [2.0, 2.1, 2.1, 2.2, 2.0, 2.5]
    N_list = [20000, 10000, 30000, 40000, 20000, 20000]

    def generate_dist(self, xmin=10, xmax=500, alpha=2.5, N=10000):
        # print("xmin ", xmin)
        count = 0
        np.random.seed(42)
        while True:
            count += 1
            syn_data = \
                np.floor((xmin-1/2)*np.power((1-np.random.uniform(0, 1, N)),
                         (1/(1-alpha))) + 1/2)
            syn_data = np.floor(np.heaviside(xmax-syn_data, 1/2) * syn_data)
            syn_data = np.delete(syn_data, np.where(syn_data == 0)[0])
            bm = np.max(syn_data) * 0.25
            alpha_syn, xmin_syn, ks_syn, Loglike_syn = \
                cr.tplfit(syn_data, bm, nfactor=0)

            if np.abs(alpha-alpha_syn) <= 0.1 and alpha_syn > 1.0:
                return xmin_syn

    def test_tplfit_new(self):
        test_output = None
        test_output = []
        for indx, xmin in enumerate(self.xmin_list):
            test_output.append(self.generate_dist(xmin=xmin,
                                                  xmax=self.xmax_list[indx],
                                                  alpha=self.alpha_list
                                                  [indx],
                                                  N=self.N_list[indx]))
        msg = "tfpfilt failed"
        for indx, xmin in enumerate(self.xmin_list):
            print("xmin ", xmin, " test_output[indx] ", test_output[indx])
            self.assertAlmostEqual(xmin, test_output[indx],
                                   msg=msg + str(xmin),
                                   delta=1)
