#!/usr/bin/env python

import os
import subprocess


class RaptorxSecstrAnalysis(object):
    def __init__(self, selected_proteins, raptorx_path,
                 fasta_path, outpath):
        self._selected_proteins = selected_proteins
        self._raptorx_path = raptorx_path
        self._fasta_path = fasta_path
        self._outpath = outpath
        
        self._selected_protein_set = set()
        
    def streamline_raptorx_secstr_analysis(self):
        '''To call from apricot'''
        self.parse_selected_data()
        self.run_raptorx_analysis()
        self.create_job_completion_file()
        
    def parse_selected_data(self):
        '''Parses selected data for uid'''
        with open(self._selected_proteins, 'r') as in_fh:
            for entry in in_fh:
                if not entry.startswith('Entry'):
                    self._selected_protein_set.add(entry.split('\t')[0])
        return self._selected_protein_set
    
    def run_raptorx_analysis(self):
        '''Runs RaptorX on the selected uids for 8-state secondary structure
        prediction

        '''
        for files in os.listdir(self._fasta_path):
            if files.split('.')[0] in self._selected_protein_set:
                print("RaptorX 8-state secondary structure analysis for %s" %
                      files)
                subprocess.Popen(
                    ["perl %s %s/%s" %
                     (self._raptorx_path, self._fasta_path, files)],
                    shell=True).wait()
                subprocess.Popen(["mv *.ss* %s" % self._outpath],
                                 shell=True).wait()
                subprocess.Popen(["mv *.horiz %s" % self._outpath],
                                 shell=True).wait()
                subprocess.Popen(["rm -rf tmp*.%s" % files.split('.')[0]],
                                 shell=True).wait()
                
    def create_job_completion_file(self):
        with open(self._outpath+'/raptorx_analysis.txt', 'w') as out_fh:
            out_fh.write("Secondary structures for the selected proteins are "
                         "generated by RaptorX.\n")
            out_fh.write("The files generated by the analysis:.\n")
            out_fh.write('\n'.join(os.listdir(self._outpath)))
