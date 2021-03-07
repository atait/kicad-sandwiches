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
L Timer:LM555xM U1
U 1 1 60410232
P 4350 3150
F 0 "U1" H 4350 3731 50  0000 C CNN
F 1 "LM555xM" H 4350 3640 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 5200 2750 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm555.pdf" H 5200 2750 50  0001 C CNN
	1    4350 3150
	1    0    0    -1  
$EndComp
$Comp
L Timer:LM555xM U2
U 1 1 60411ADA
P 6950 3200
F 0 "U2" H 6950 3781 50  0000 C CNN
F 1 "LM555xM" H 6950 3690 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 7800 2800 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm555.pdf" H 7800 2800 50  0001 C CNN
	1    6950 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 2950 3550 2950
Wire Wire Line
	3550 2950 3550 3800
Wire Wire Line
	3550 3800 6950 3800
Wire Wire Line
	6950 3800 6950 3600
Wire Wire Line
	4850 2950 6100 2950
Wire Wire Line
	6100 2950 6100 3200
Wire Wire Line
	6100 3200 6450 3200
$Comp
L Graphic:SYM_Magnet_Small G1
U 1 1 60412CA6
P 5550 1900
F 0 "G1" H 5550 2040 50  0001 C CNN
F 1 "KISANDWICH-MIDBOARD" H 5550 1775 50  0001 C CNN
F 2 "Alex_Graphics:cat_02" H 5550 1725 50  0001 C CNN
F 3 "~" H 5580 1700 50  0001 C CNN
	1    5550 1900
	1    0    0    -1  
$EndComp
$Comp
L Device:Speaker LS101
U 1 1 6044355E
P 4000 4850
F 0 "LS101" H 4170 4846 50  0000 L CNN
F 1 "KISANDWICH-MIDBOARD" H 4170 4755 50  0000 L CNN
F 2 "Alex_Connectors:Speaker_CUI_CLS0281MAE_embedded" H 4000 4650 50  0001 C CNN
F 3 "~" H 3990 4800 50  0001 C CNN
	1    4000 4850
	1    0    0    -1  
$EndComp
$Comp
L sandwich-features:Speaker-cutout-3board KS101
U 1 1 60443B6A
P 4000 4900
F 0 "KS101" H 4000 4900 50  0001 C CNN
F 1 "KISANDWICH-CUTTER" H 4378 4900 50  0000 L CNN
F 2 "Alex_Connectors:CUI-speaker-3layer-tight" H 4000 4900 50  0001 C CNN
F 3 "" H 4000 4900 50  0001 C CNN
	1    4000 4900
	1    0    0    -1  
$EndComp
$EndSCHEMATC
