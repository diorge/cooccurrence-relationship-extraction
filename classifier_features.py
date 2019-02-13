import os
import pandas as pd
from collections import defaultdict


class InstanceFrequencyCount:
    """Returns the mean of the frequency
    of the instances of the two categories.
    In other words, how common are the
    instances of the categories, on average.

    Uses the raw SVO because it doesn't
    require both S and O to be each of
    one category.
    """
    def __init__(self, cache=False):
        self.cache = cache

    def __repr__(self):
        return 'InstanceFrequencyCount'

    def __str__(self):
        return repr(self)

    def required_files(self):
        return ['svo']

    def required_data(self):
        return ['cat1', 'cat2']

    def creates(self):
        return ['instance_frequency_cat1', 'instance_frequency_cat2']

    def returns(self):
        return ['mean_instance_frequency_cat1', 'mean_instance_frequency_cat2']

    def apply(self, svo, cat1, cat2, output_dir, **kwargs):
        frequencies1 = self.count(svo, cat1)
        frequencies2 = self.count(svo, cat2)
        
        freq1_df = pd.DataFrame({'instance': list(frequencies1.keys()),
                                 'frequency': list(frequencies1.values())})
        freq2_df = pd.DataFrame({'instance': list(frequencies2.keys()),
                                 'frequency': list(frequencies2.values())})

        # "normalizes" by settings the range 0-1 linearly,
        # ie. divides by the maximum
        freq1_df['normalized'] = freq1_df['frequency'] / freq1_df['frequency'].max()
        freq2_df['normalized'] = freq2_df['frequency'] / freq2_df['frequency'].max()

        # save intermediate step for later inspection
        freq1_df.to_csv(os.path.join(output_dir, 'instance_frequency_cat1'), index=False)
        freq2_df.to_csv(os.path.join(output_dir, 'instance_frequency_cat2'), index=False)

        # actual feature
        mean1 = freq1_df['normalized'].mean()
        mean2 = freq2_df['normalized'].mean()

        return {'mean_instance_frequency_cat1': mean1,
                'mean_instance_frequency_cat2': mean2}

    def count(self, svo, instances):
        counter = defaultdict(lambda: 0)

        with open(svo) as svo_contents:
            for line in svo_contents:
                s, v, o, n = line.split('\t')

                if s in instances:
                    counter[s] += int(n)
                if o in instances:
                    counter[o] += int(n)

        return counter