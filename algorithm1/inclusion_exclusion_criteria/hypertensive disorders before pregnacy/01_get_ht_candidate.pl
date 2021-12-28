use strict;
use warnings;
use Text::ParseWords;
use utf8;
use Encode;

my $file = "clinical_notes.csv";
my $out = "ht_candidate.csv";
my $target_itemcd = "000001"; #item code of the interview of first visit
my %dict;
my %dict2;
open(my $OUT,'>:encoding(UTF-8)',$out) or die "$!";
open(my $FH, '<:encoding(UTF-8)', $file) or die "$!";

while(my $line = <$FH>){
	chomp($line);
	my @splited_line = &parse_line(",", undef, $line);		
	if($splited_line[1] eq $target_itemcd){
		my $sentence = $splited_line[6];
		my $jid = $splited_line[12];
		if($sentence =~ /高血圧/){
			print $OUT $jid,",",$sentence,"\n";

		}
		elsif($sentence =~ /血圧/){
			print $OUT $jid,",",$sentence,"\n";

		}
		elsif($sentence =~ /白衣/){
			print $OUT $jid,",",$sentence,"\n";

		}
		elsif($sentence =~ /アダラート/){
			print $OUT $jid,",",$sentence,"\n";

		}
		elsif($sentence =~ /アムロジン/){
			print $OUT $jid,",",$sentence,"\n";

		}
		elsif($sentence =~ /オルメテック/){
			print $OUT $jid,",",$sentence,"\n";

		}		
		elsif($sentence =~ /アルドメット/){
			print $OUT $jid,",",$sentence,"\n";

		}	
		elsif($sentence =~ /トランデート/){
			print $OUT $jid,",",$sentence,"\n";
		}	
		elsif($sentence =~ /ナトリックス/){
			print $OUT $jid,",",$sentence,"\n";
		}		
		elsif($sentence =~ /HT/){
			print $OUT $jid,",",$sentence,"\n";

		}
		elsif($sentence =~ /降圧/){
			print $OUT $jid,",",$sentence,"\n";
		}	
		elsif($sentence =~ /ニフェジピン/){
			print $OUT $jid,",",$sentence,"\n";
		}
		elsif($sentence =~ /アプレゾリン/){
			print $OUT $jid,",",$sentence,"\n";
		}
		elsif($sentence =~ /アルデステロン/){
			print $OUT $jid,",",$sentence,"\n";
		}
		elsif($sentence =~ /腎高内/){
			print $OUT $jid,",",$sentence,"\n";
		}		
	}	
}
