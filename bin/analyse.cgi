#!/usr/bin/env perl

use warnings;
use strict;

use Path::Tiny qw/path/;
use feature qw/say/;

use Data::Dumper::Simple;
use Text::CSV_XS;

# -------------------- Metrics -------------------------- @
my $all = 13983816;
my $sums = {};

$sums->{$_} = { 'percent' => 0, 'count' => 0 } for (21..279);

my $metrics = {
	'all' => $all,
	'even_odd' => { '6-0' => { 'percent' => 0, 'count' => 0 }, '5-1' => { 'percent' => 0, 'count' => 0 }, '4-2' => { 'percent' => 0, 'count' => 0 }, '3-3' => { 'percent' => 0, 'count' => 0 }, '2-4'=> { 'percent' => 0, 'count' => 0 }, '1-5' => { 'percent' => 0, 'count' => 0 }, '0-6' => { 'percent' => 0, 'count' => 0 }},
	'low_high' => { '6-0' => { 'percent' => 0, 'count' => 0 }, '5-1' => { 'percent' => 0, 'count' => 0 }, '4-2' => { 'percent' => 0, 'count' => 0 }, '3-3' => { 'percent' => 0, 'count' => 0 }, '2-4'=> { 'percent' => 0, 'count' => 0 }, '1-5' => { 'percent' => 0, 'count' => 0 }, '0-6' => { 'percent' => 0, 'count' => 0 }},
	'sum' => $sums,
	'numbers_same_ending_digit' => {'0' => { 'percent' => 0, 'count' => 0 }, '1' => { 'percent' => 0, 'count' => 0 }, '2' => { 'percent' => 0, 'count' => 0 }, '3' => { 'percent' => 0, 'count' => 0 }, '4' => { 'percent' => 0, 'count' => 0 }, '5' => { 'percent' => 0, 'count' => 0 }, '6' => { 'percent' => 0, 'count' => 0 }}

};


my $csv = Text::CSV_XS->new ({ binary => 1, auto_diag => 1 });
open my $fh, "<:encoding(utf8)", "649.all.csv" or die "649.all.csv: $!";

my @cols = @{$csv->getline ($fh)};
my $row = {};
$csv->bind_columns (\@{$row}{@cols});
while ($csv->getline ($fh)) {

		$metrics->{sum}->{$row->{sum}}->{count} ++;
		# ending digit
		# my @digits = split(/-/, $row->{ending_digit} );
		# $metrics->{'ending_digit'}->{$_} += $digits[$_] for (0..9);

		# rest of metrics
		$metrics->{$_}->{$row->{$_}}->{count}++ for ('even_odd','low_high', 'numbers_same_ending_digit');
}

# add percentage
foreach my $sets ('sum','even_odd','low_high', 'numbers_same_ending_digit'){

	$metrics->{$sets}->{$_}->{percent} = int(($metrics->{$sets}->{$_}->{count}/$all)*100) for (keys %{$metrics->{$sets}})

}
#for ('sum','even_odd','low_high', 'numbers_same_ending_digit');

say path('log.txt')->spew(Dumper($metrics));
