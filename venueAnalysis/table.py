from collections import Counter

l1=['HICSS', 'IEEE Intell. Syst.', 'Soc. Networks', 'CHI Extended Abstracts', 'SMC', 'Web Intelligence', 'IEEE Pervasive Comput.', 'IEEE Softw.', 'WWW', 'ISI', 'IEEE Trans. Engineering Management', 'Computer', 'Expert Syst. Appl.', 'CHI', 'KDD', 'PAKDD', 'CSCW', 'IEEE Internet Comput.', 'IEEE Trans. Syst. Man Cybern. Part C', 'ICAIL']



l2=['ASONAM', 'Comput. Hum. Behav.', 'HICSS', 'WWW (Companion Volume)', 'SocialCom/PASSAT', 'CIKM', 'WWW', 'CHI', 'CSCW', 'Soc. Netw. Anal. Min.', 'CHI Extended Abstracts', 'Expert Syst. Appl.', 'IEEE Trans. Multim.', 'GLOBECOM', 'ACM Multimedia', 'SBP', 'SocInfo', 'SocialCom', 'CSE (4)', 'INFOCOM']



l3=['IEEE Access', 'ASONAM', 'IEEE BigData', 'Soc. Netw. Anal. Min.', 'CHI', 'WWW (Companion Volume)', 'IEEE Trans. Comput. Soc. Syst.', 'Telematics Informatics', 'Multim. Tools Appl.', 'Proc. ACM Hum. Comput. Interact.', 'Expert Syst. Appl.', 'HICSS', 'IEEE Trans. Multim.', 'Int. J. Inf. Manag.', 'IEEE Trans. Knowl. Data Eng.', 'SMSociety', 'ICC', 'Knowl. Based Syst.', 'CIKM', 'WWW']



l4=['IEEE Access', 'ASONAM', 'HICSS', 'WWW (Companion Volume)', 'Soc. Netw. Anal. Min.', 'Comput. Hum. Behav.', 'CHI', 'IEEE BigData', 'CIKM', 'Expert Syst. Appl.', 'WWW', 'IEEE Trans. Multim.', 'CHI Extended Abstracts', 'Multim. Tools Appl.', 'Telematics Informatics', 'IEEE Trans. Comput. Soc. Syst.', 'CSCW', 'GLOBECOM', 'Soc. Networks', 'ICC']






l = l1+l2+l3

b = dict(Counter(l))
print ([key for key,value in b.items()if value > 1]) #只展示重复元素
print ({key:value for key,value in b.items()if value > 1}) #展现重复元素和重复次数
