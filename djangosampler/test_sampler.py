from __future__ import absolute_import

from time import sleep
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.test import TestCase
from django.db.utils import DatabaseError

from . import sampler
from . import models


class TestCalculateCost(TestCase):

    @patch('djangosampler.sampler.USE_COST', False)
    def test_use_cost_false_returns_zero(self):
        self.assertEquals(0.0, sampler._calculate_cost(1))

    @patch('djangosampler.sampler.USE_COST', True)
    @patch('djangosampler.sampler.FREQ', 0)
    def test_use_cost_true_freq_zero(self):
        self.assertEquals(0.005, sampler._calculate_cost(1))

    @patch('djangosampler.sampler.USE_COST', True)
    @patch('djangosampler.sampler.FREQ', 0.5)
    def test_use_cost_true_freq_non_zero_float(self):
        self.assertEquals(0.5, sampler._calculate_cost(1))

    @patch('djangosampler.sampler.USE_COST', True)
    @patch('djangosampler.sampler.FREQ', 1)
    def test_use_cost_true_freq_non_zero_int(self):
        self.assertEquals(1.0, sampler._calculate_cost(1))

    @patch('djangosampler.sampler.USE_COST', True)
    @patch('djangosampler.sampler.FREQ', 0.5)
    @patch('djangosampler.sampler.BASE_TIME', 1)
    def test_use_cost_true_base_time_int(self):
        self.assertEquals(1.0, sampler._calculate_cost(1))


class TestSampler(TestCase):

    def test_sample(self):
        sampler.sample('sql', 'SELECT 1', 1, [])

        query = models.Query.objects.get()
        self.assertEquals('sql', query.query_type)
        self.assertEquals('SELECT 1', query.query)
        self.assertEquals(0.0, query.total_cost)
        self.assertEquals(1.0, query.total_duration)
        self.assertEquals(1, query.count)

    @patch('djangosampler.sampler.USE_COST', True)
    def test_sample_use_cost_true(self):
        sampler.sample('sql', 'SELECT 1', 1, [])

        query = models.Query.objects.get()
        self.assertEquals('sql', query.query_type)
        self.assertEquals('SELECT 1', query.query)
        self.assertEquals(0.005, query.total_cost)
        self.assertEquals(1.0, query.total_duration)
        self.assertEquals(1, query.count)

    @patch('djangosampler.sampler.Query', autospec=True)
    def test_query_get_or_create_db_error(self, mock_query):
        mock_query.objects.get_or_create.side_effect = DatabaseError

        self.assertIsNone(sampler.sample('sql', 'SELECT 1', 1, []))

    @patch('djangosampler.sampler.Stack', autospec=True)
    def test_stack_get_or_create_db_error(self, mock_stack):
        mock_stack.objects.get_or_create.side_effect = DatabaseError

        self.assertIsNone(sampler.sample('sql', 'SELECT 1', 1, []))

    @patch('djangosampler.sampler.Sample', autospec=True)
    def test_sample_create_db_error(self, mock_stack):
        mock_stack.objects.create.side_effect = DatabaseError

        self.assertIsNone(sampler.sample('sql', 'SELECT 1', 1, []))


class TestSamplingContextManager(TestCase):
    def test_with(self):
        sampler.FREQ = 1

        with sampler.sampling('bob', 'baz', ('foo', 'foobar')):
            sleep(0.01)

        query = models.Query.objects.get()
        self.assertEquals('bob', query.query_type)
        self.assertEquals('baz', query.query)
        self.assertTrue(query.total_duration >= 0.01)
