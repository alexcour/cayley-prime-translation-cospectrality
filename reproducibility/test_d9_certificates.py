#!/usr/bin/env python3
"""Reject corrupted finite certificates; no GI or producer imported."""
import copy
import json
from pathlib import Path
import unittest

import check_d9_certificates as checker


class CorruptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).parent/'results/d9_certificates_20261021/certificate.json'
        cls.original=json.loads(path.read_text())

    def altered(self):
        return copy.deepcopy(self.original)

    def test_missing_member(self):
        c=self.altered();c['members'].pop()
        with self.assertRaisesRegex(ValueError,'number of membership'):
            checker.check(c)

    def test_duplicate_support(self):
        c=self.altered();c['members'][1]=copy.deepcopy(c['members'][0])
        with self.assertRaisesRegex(ValueError,'duplicated or extraneous'):
            checker.check(c)

    def test_nonpermutation(self):
        c=self.altered();c['members'][0]['vertex_image'][0]=c['members'][0]['vertex_image'][1]
        with self.assertRaisesRegex(ValueError,'Not a permutation'):
            checker.check(c)

    def test_bijective_wrong_graph_map(self):
        c=self.altered()
        # A genuine group automorphism but not a map to the claimed representative.
        c['members'][0]['automorphism']={'u':1,'v':1}
        c['members'][0]['vertex_image']=[(x%9+x//9)%9+9*(x//9) for x in range(18)]
        with self.assertRaisesRegex(ValueError,'adjacency permutation mismatch'):
            checker.check(c)

    def test_polynomial_corruption(self):
        c=self.altered();c['classes'][0]['charpoly_descending'][-1]+=1
        with self.assertRaisesRegex(ValueError,'polynomial determinant mismatch'):
            checker.check(c)

    def test_trace_corruption(self):
        c=self.altered();c['classes'][0]['traces_1_to_18'][5]+=1
        with self.assertRaisesRegex(ValueError,'Trace certificate mismatch'):
            checker.check(c)

    def test_motif_corruption(self):
        c=self.altered();c['classes'][0]['motif4'][0][1]+=1
        with self.assertRaisesRegex(ValueError,'Four-motif certificate mismatch'):
            checker.check(c)

    def test_false_pair_certificate(self):
        c=self.altered();c['pair_separation'][0]['values'][0]+=1
        with self.assertRaisesRegex(ValueError,'Invalid nonisomorphism certificate'):
            checker.check(c)

    def test_bareiss_row_swap_and_singular(self):
        self.assertEqual(checker.bareiss_det([[0,1],[2,3]]),-2)
        self.assertEqual(checker.bareiss_det([[1,2],[2,4]]),0)


if __name__=='__main__':
    unittest.main()
