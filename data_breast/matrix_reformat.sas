filename in1 'C:\Users\Liz\Documents\Liz's\04Professional\masters_degree\CS598_DeepLearningHealthcare\proj\try1\data_Breast-noDetroit-allLA-ASCII_250406-1620\matrix.txt';
                                                                                      
data in;                                                                              
  infile seer9 lrecl=300;                                                             
  input                                                                                   
    @ 1   PUBCSNUM             $char8.  /* Patient ID */ 
    @ 9   MAR_STAT             $char1.  /* Marital status at diagnosis */ 
    @ 10  RACE1V               $char2.  /* Race/ethnicity */ 
    @ 12  SEX                  $char1.  /* Sex */ 
    @ 13  AGE_DX               $char3.  /* Age recode with single ages and 90+ */ 
    @ 16  YR_BRTH              $char4.  /* Year of birth */ 
    @ 20  SEQ_NUM              $char2.  /* Sequence number */ 
    @ 22  YEAR_DX              $char3.  /* Year of diagnosis */ 
    @ 25  PRIMSITE             $char3.  /* Primary Site */ 
    @ 28  LATERAL              $char1.  /* Laterality */ 
    @ 29  HISTO3V              $char4.  /* Histologic Type ICD-O-3 */ 
    @ 33  BEHO3V               $char1.  /* Behavior code ICD-O-3 */ 
    @ 34  GRADE                $char1.  /* Grade Recode (thru 2017) */ 
    @ 35  DX_CONF              $char1.  /* Diagnostic Confirmation */ 
    @ 36  REPT_SRC             $char1.  /* Type of Reporting Source */ 
    @ 37  EOD10_SZ             $char4.  /* EOD 10 - size (1988-2003) */ 
    @ 41  EOD10_EX             $char3.  /* EOD 10 - extent (1988-2003) */ 
    @ 44  EOD10_PE             $char3.  /* EOD 10 - Prostate path ext (1995-2003) */ 
    @ 47  EOD10_ND             $char2.  /* EOD 10 - nodes (1988-2003) */ 
    @ 49  EOD10_PN             $char2.  /* Regional nodes positive (1988+) */ 
    @ 51  EOD10_NE             $char2.  /* Regional nodes examined (1988+) */ 
    @ 53  EOD_CODE             $char1.  /* Coding system-EOD (1973-2003) */ 
    @ 54  TUMOR_1V             $char2.  /* Tumor marker 1 (1990-2003) */ 
    @ 56  TUMOR_2V             $char2.  /* Tumor marker 2 (1990-2003) */ 
    @ 58  TUMOR_3V             $char2.  /* Tumor marker 3 (1998-2003) */ 
    @ 60  CSTUMSIZ             $char4.  /* CS tumor size (2004-2015) */ 
    @ 64  CSEXTEN              $char4.  /* CS extension (2004-2015) */ 
    @ 68  CSLYMPHN             $char4.  /* CS lymph nodes (2004-2015) */ 
    @ 72  CSMETSDX             $char3.  /* CS mets at dx (2004-2015) */ 
    @ 75  CS1SITE              $char4.  /* CS site-specific factor 1 (2004-2017 varying by schema) */ 
    @ 79  CS2SITE              $char4.  /* CS site-specific factor 2 (2004-2017 varying by schema) */ 
    @ 83  CS3SITE              $char4.  /* CS site-specific factor 3 (2004-2017 varying by schema) */ 
    @ 87  CS4SITE              $char4.  /* CS site-specific factor 4 (2004-2017 varying by schema) */ 
    @ 91  CS5SITE              $char4.  /* CS site-specific factor 5 (2004-2017 varying by schema) */ 
    @ 95  CS6SITE              $char4.  /* CS site-specific factor 6 (2004-2017 varying by schema) */ 
    @ 99  CS25SITE             $char4.  /* CS site-specific factor 25 (2004-2017 varying by schema) */ 
    @ 103 DAJCCT               $char3.  /* Derived AJCC T, 6th ed (2004-2015) */ 
    @ 106 DAJCCN               $char3.  /* Derived AJCC N, 6th ed (2004-2015) */ 
    @ 109 DAJCCM               $char3.  /* Derived AJCC M, 6th ed (2004-2015) */ 
    @ 112 DAJCCSTG             $char3.  /* Derived AJCC Stage Group, 6th ed (2004-2015) */ 
    @ 115 DSS2000S             $char2.  /* SEER Combined Summary Stage 2000 (2004-2017) */ 
    @ 117 CSVFIRST             $char2.  /* CS version input original (2004-2015) */ 
    @ 119 CSVLATES             $char2.  /* CS version derived (2004-2015) */ 
    @ 121 CSVCURRENT           $char2.  /* CS version input current (2004-2015) */ 
    @ 123 SURGPRIF             $char2.  /* RX Summ--Surg Prim Site (1998+) */ 
    @ 125 SURGSCOF             $char2.  /* RX Summ--Scope Reg LN Sur (2003+) */ 
    @ 127 SURGSITF             $char2.  /* RX Summ--Surg Oth Reg/Dis (2003+) */ 
    @ 129 NUMNODES             $char3.  /* RX Summ--Reg LN Examined (1998-2002) */ 
    @ 132 NO_SURG              $char1.  /* Reason no cancer-directed surgery */ 
    @ 133 SS_SURG              $char3.  /* Site specific surgery (1973-1997 varying detail by year and site) */ 
    @ 136 SURGSCOP             $char2.  /* Scope of reg lymph nd surg (1998-2002) */ 
    @ 138 SURGSITE             $char2.  /* Surgery of oth reg/dis sites (1998-2002) */ 
    @ 140 REC_NO               $char2.  /* Record number recode */ 
    @ 142 AGE_1REC             $char2.  /* Age recode with <1 year olds */ 
    @ 144 SITERWHO             $char2.  /* Site recode ICD-O-3/WHO 2008 */ 
    @ 146 ICCC3WHO             $char3.  /* ICCC site recode 3rd edition/IARC 2017 */ 
    @ 149 ICCC3XWHO            $char3.  /* ICCC site recode extended 3rd edition/IARC 2017 */ 
    @ 152 BEHTREND             $char1.  /* Behavior recode for analysis */ 
    @ 153 HISTREC              $char2.  /* Histology recode - broad groupings */ 
    @ 155 HISTRECB             $char2.  /* SEER Brain and CNS Recode */ 
    @ 157 CS0204SCHEMA         $char3.  /* TNM 7/CS v0204+ Schema (thru 2017) */ 
    @ 160 RAC_RECA             $char1.  /* Race recode (White, Black, Other) */ 
    @ 161 RAC_RECY             $char1.  /* Race recode (W, B, AI, API) */ 
    @ 162 ORIGRECB             $char1.  /* Origin recode NHIA (Hispanic, Non-Hisp) */ 
    @ 163 HST_STGA             $char2.  /* SEER historic stage A (1973-2015) */ 
    @ 165 AJCC_STG             $char3.  /* AJCC stage 3rd edition (1988-2003) */ 
    @ 168 AJ_3SEER             $char3.  /* SEER modified AJCC stage 3rd (1988-2003) */ 
    @ 171 SSSM2KPZ             $char2.  /* Combined Summary Stage (2004+) */ 
    @ 173 FIRSTPRM             $char1.  /* First malignant primary indicator */ 
    @ 174 CODPUB               $char3.  /* COD to site recode */ 
    @ 177 CODPUBKM             $char3.  /* COD to site rec KM */ 
    @ 180 STAT_REC             $char1.  /* Vital status recode (study cutoff used) */ 
    @ 181 IHSLINK              $char1.  /* IHS Link */ 
    @ 182 SUMM2K               $char2.  /* Summary stage 2000 (1998-2017) */ 
    @ 184 AYASITERWHO          $char3.  /* AYA site recode 2020 Revision */ 
    @ 187 LYMSUBRWHO           $char2.  /* Lymphoid neoplasm recode 2021 Revision */ 
    @ 189 VSRTSADX             $char1.  /* SEER cause-specific death classification */ 
    @ 190 ODTHCLASS            $char1.  /* SEER other cause of death classification */ 
    @ 191 CSTSEVAL             $char2.  /* CS Tumor Size/Ext Eval (2004-2015) */ 
    @ 193 CSRGEVAL             $char2.  /* CS Reg Node Eval (2004-2015) */ 
    @ 195 CSMTEVAL             $char2.  /* CS Mets Eval (2004-2015) */ 
    @ 197 INTPRIM              $char1.  /* Primary by international rules */ 
    @ 198 ERSTATUS             $char1.  /* ER Status Recode Breast Cancer (1990+) */ 
    @ 199 PRSTATUS             $char1.  /* PR Status Recode Breast Cancer (1990+) */ 
    @ 200 CSSCHEMA             $char2.  /* CS Schema - AJCC 6th Edition */ 
    @ 202 CS8SITE              $char4.  /* CS site-specific factor 8 (2004-2017 varying by schema) */ 
    @ 206 CS10SITE             $char4.  /* CS site-specific factor 10 (2004-2017 varying by schema) */ 
    @ 210 CS11SITE             $char4.  /* CS site-specific factor 11 (2004-2017 varying by schema) */ 
    @ 214 CS13SITE             $char4.  /* CS site-specific factor 13 (2004-2017 varying by schema) */ 
    @ 218 CS15SITE             $char4.  /* CS site-specific factor 15 (2004-2017 varying by schema) */ 
    @ 222 CS16SITE             $char4.  /* CS site-specific factor 16 (2004-2017 varying by schema) */ 
    @ 226 VASINV               $char2.  /* Lymph-vascular Invasion (2004+ varying by schema) */ 
    @ 228 SRV_TIME_MON         $char4.  /* Survival months */ 
    @ 232 SRV_TIME_MON_FLAG    $char1.  /* Survival months flag */ 
    @ 233 DAJCC7T              $char4.  /* Derived AJCC T, 7th ed (2010-2015) */ 
    @ 237 DAJCC7N              $char4.  /* Derived AJCC N, 7th ed (2010-2015) */ 
    @ 241 DAJCC7M              $char4.  /* Derived AJCC M, 7th ed (2010-2015) */ 
    @ 245 DAJCC7STG            $char4.  /* Derived AJCC Stage Group, 7th ed (2010-2015) */ 
    @ 249 ADJTM_6VALUE         $char3.  /* Breast - Adjusted AJCC 6th T (1988-2015) */ 
    @ 252 ADJNM_6VALUE         $char3.  /* Breast - Adjusted AJCC 6th N (1988-2015) */ 
    @ 255 ADJM_6VALUE          $char3.  /* Breast - Adjusted AJCC 6th M (1988-2015) */ 
    @ 258 ADJAJCCSTG           $char3.  /* Breast - Adjusted AJCC 6th Stage (1988-2015) */ 
    @ 261 CS7SITE              $char3.  /* Adjusted CS site-specific factor 7 (2004-2017 varying by schema) */ 
    @ 264 CS9SITE              $char4.  /* CS site-specific factor 9 (2004-2017 varying by schema) */ 
    @ 268 CS12SITE             $char4.  /* CS site-specific factor 12 (2004-2017 varying by schema) */ 
    @ 272 HER2                 $char1.  /* Derived HER2 Recode (2010+) */ 
    @ 273 BRST_SUB             $char1.  /* Breast Subtype (2010+) */ 
    @ 274 ANNARBOR             $char2.  /* Lymphoma - Ann Arbor Stage (1983-2015) */ 
    @ 276 CSMETSDXB_PUB        $char2.  /* SEER Combined Mets at DX-bone (2010+) */ 
    @ 278 CSMETSDXBR_PUB       $char2.  /* SEER Combined Mets at DX-brain (2010+) */ 
    @ 280 CSMETSDXLIV_PUB      $char2.  /* SEER Combined Mets at DX-liver (2010+) */ 
    @ 282 CSMETSDXLUNG_PUB     $char2.  /* SEER Combined Mets at DX-lung (2010+) */ 
    @ 284 T_VALUE              $char3.  /* T value - based on AJCC 3rd (1988-2003) */ 
    @ 287 N_VALUE              $char3.  /* N value - based on AJCC 3rd (1988-2003) */ 
    @ 290 M_VALUE              $char3.  /* M value - based on AJCC 3rd (1988-2003) */ 
    @ 293 MALIGCOUNT           $char2.  /* Total number of in situ/malignant tumors for patient */ 
    @ 295 BENBORDCOUNT         $char2.  /* Total number of benign/borderline tumors for patient */ 
    @ 297 XMHIIA               $char2.  /* Median household income inflation adj to 2022 */ 
    @ 299 XRUCC                $char2.  /* Rural-Urban Continuum Code */ 										 ; 
	