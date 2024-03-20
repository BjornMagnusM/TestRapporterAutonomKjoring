t=out.tout; %Makes a time variable from simulink 
outputHIV=out.ScopeDataHIV.signals.values(:,1); %Makes an output varible for hiv motion 
inputHIV=out.ScopeDataHIV.signals.values(:,2); %Makes an input varible for hiv motion 

outputGIR=out.ScopeDataGIR.signals.values(:,1); %Makes an output varible for gir motion 
inputGIR=out.ScopeDataGIR.signals.values(:,2); %Makes an input varible for git motion

outputJAG=out.ScopeDataJAG.signals.values(:,1); %Makes an output varible for jag motion 
inputJAG=out.ScopeDataJAG.signals.values(:,2); %Makes an input varible for jag motion

outputSVEI=out.ScopeDataSVEI.signals.values(:,1); %Makes an output varible for svei motion 
inputSVEI=out.ScopeDataSVEI.signals.values(:,2); %Makes an input varible for sveiv motion

systemIdentification
