import test_fasta
import os
import screed
from screed.DBConstants import fileExtension
import screed_tst_utils as utils
import shutil

class Test_fasta_to_fastq(test_fasta.Test_fasta):

    """
    Tests the ability to convert a fasta db to a fastq file, parse it into
    a fastq db, save to a fasta file, parse the fasta file into a fasta
    db and then run the fasta suite
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)
        
        temp_fa2fq = utils.get_temp_filename('fa_to_fq')
        # shutil.copy(os.path.join(thisdir, 'fa_to_fq'), temp_fa2fq)
        self._fqName = temp_fa2fq

        temp_fq2fa = utils.get_temp_filename('fq_to_fa')
        # shutil.copy(os.path.join(thisdir, 'fq_to_fa'), temp_fq2fa)
        self._faName = temp_fq2fa
        
        tempfasta = utils.get_temp_filename('test.fa')
        shutil.copy(os.path.join(thisdir, 'test.fa'), tempfasta)
        self._testfa = tempfasta
        
        screed.read_fasta_sequences(self._testfa)
        screed.ToFastq(self._testfa, self._fqName)  # Fasta db -> fasta text
        screed.read_fastq_sequences(self._fqName)  # Fastq file -> fastq db
        screed.ToFasta(self._fqName, self._faName)  # Fastq db -> fasta text
        screed.read_fasta_sequences(self._faName)  # Fasta file -> fasta db
        self.db = screed.ScreedDB(self._faName)

    def teardown(self):
        os.unlink(self._fqName)
        os.unlink(self._fqName + fileExtension)
        os.unlink(self._faName)
        os.unlink(self._faName + fileExtension)
        os.unlink(self._testfa + fileExtension)
