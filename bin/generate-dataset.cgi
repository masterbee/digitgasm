#!/usr/bin/env perl

use warnings;
use strict;

use Path::Tiny qw/path/;
use feature qw/say/;
use Math::Combinatorics;
use List::AllUtils qw( :all );


 
my @n = (1 .. 49);
my $combinat = Math::Combinatorics->new(count => 6,
                                        data => [@n],
                                       );
 
 my $csv = path('649.all.csv');
 $csv->spew_raw(
 	join(",",("slot_1", "slot_2", "slot_3", "slot_4", "slot_5", "slot_6", "sum", "low_high", "numbers_same_ending_digit", "even_odd")),
 	"\n"
 	);
while(my @combo = $combinat->next_combination){
  my $sum = sum0(@combo);
  my $high_low = high_low(@combo);
  my $last_element = same_ending_digit(@combo);
  my $odd_even = odd_even(@combo);
  push(@combo, $_) for ($sum,$high_low,$last_element,$odd_even);
  $csv->append_raw(
  		join(',',@combo),"\n"
  );
}


sub high_low {
	my @args = @_;
	my @low = indexes { $_ < 25 } @args;
	my @high = indexes { $_ > 24 } @args;
	return join("-",(scalar(@low), scalar(@high)));
}

sub odd_even {
	my @args = @_;
	my @even = indexes { $_ % 2 == 0 } @args;
	my @odd = indexes { $_ % 2 != 0 } @args;
	return join("-",(scalar(@even), scalar(@odd)));
}


sub same_ending_digit {
	my @args = @_;
	my @spread = (0,0,0,0,0,0,0,0,0,0);
	foreach my $num (@args)
	{
		my ($last) = $num =~ /(\d)$/;
		$spread[$last]++;
	}

	my $highest = max @spread;

	return ( $highest > 1 ) ? $highest : 0
}	



