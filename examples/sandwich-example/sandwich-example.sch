EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Timer:LM555xM U2
U 1 1 601C92C0
P 5200 4050
F 0 "U2" H 5200 4631 50  0000 C CNN
F 1 "LM555xM" H 5200 4540 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 6050 3650 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm555.pdf" H 6050 3650 50  0001 C CNN
	1    5200 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 3850 4600 3850
Wire Wire Line
	4600 3850 4600 4050
Wire Wire Line
	4600 4050 4700 4050
Wire Wire Line
	3150 3850 3000 3850
Wire Wire Line
	3000 3850 3000 4600
Wire Wire Line
	5200 4450 5200 4600
Wire Wire Line
	5200 4600 3000 4600
$Comp
L Timer:LM555xM U1
U 1 1 601C8A32
P 3650 4050
F 0 "U1" H 3650 4631 50  0000 C CNN
F 1 "LM555xM" H 3650 4540 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 4500 3650 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm555.pdf" H 4500 3650 50  0001 C CNN
	1    3650 4050
	1    0    0    -1  
$EndComp
$EndSCHEMATC
