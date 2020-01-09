# graphhopper
graphhopper routing service on arnaud
## Quickstart
start a new tmux session:
```
tmux new -s ghop
```
start the graphopper server:
```
java -Dgraphhopper.datareader.file=/backup/mbap_shared/osm_roads/north-america-latest.osm.pbf -jar graphhopper-web-0.12.0.jar server config-example.yml
```
detatch from ghop session
```
[ctrl + b] + d
```
test that the routing server is working:
```
curl 'http://localhost:8989/route/?point=37.879189,-93.587036&point=37.274053,-93.24646'
```
should return:
```
{"hints":{"visited_nodes.average":"168.0","visited_nodes.sum":"168"},"info":{"copyrights":["GraphHopper","OpenStreetMap contributors"],"took":6},"paths":[{"distance":91474.111,"weight":3941.07384,"time":3941009,"transfers":0,"points_encoded":true,"bbox":[-93.623242,37.248825,-93.246491,37.887571],"points":"mhefFl|fzPMFKNANAhCYxWItWG\\GPQF{S_@SDGLCRKnLo@b`@E`@M^[ZQ^s@|BOZURu@LaECaA@WNmAbBc@d@[P]d@Ul@o@dCGjFSxKIfOCv@IjIKtLtO]da@eBvA[dCyApIaHtCaBtGiArB?xA`@h@j@v@rAXvBAdFzIa@dZcB~s@uChVmAviDkOdHkAbIsBrGmCvHoE~F{Ena@y`@nw@{u@bb@ua@dVeUlIoId]{\\`y@ow@nt@kr@tm@{m@lb@_a@nDwChPyKb^oUhc@wYbyAc`Alz@kk@xwAo_AjZmSvVeP|UkPfp@wb@zWgQ~V_PxOqKjVePbYmQ~NwJ~QoMjMcIvYkR`O{Jji@u]jOcK~HqF`e@iZvJ{G`dCc`BhZoSrPsKpEmC~NsJxMaJfZaSpDqC|FuFvA{AjCeDdA}A`EiHhCqF`cA}tCnBaEjBqD|D}G`CyCfCsCzCyCvAiAnBkArBeAnDmA|n@oRjJuDd{@oa@dkAej@vtAgb@`HmCvEwB~TsLjMqGpNsH`LwF|c@sUlj@gYrH_EjCoA|U}LnQ{IlDoAvA[lD]lCI|GTvWf@vYJrCRvB?pBF~GD`BN`EDzJBjFZdpAdBzzAdCxEApLb@pKPhDK~L\\~ED~Ic@jDKlRaBxKs@bBQfAWdEoAhCuAbTiNdJsFhBq@fBe@bDk@zBWlBEn|BnExBE|AKnBYpB_@thBgo@zh@gRp[}K~TeI`iAy`@`Ck@pCY`DQr|AvBlgCtDvmA|A`T\\nBCnCUpDk@dG{At{@uRddBu_@pBu@pDkBfCqBtBoBbB{BdBiBri@mp@hAy@hAo@t@YrA_@pAQhAGjA@tCNfDDpAAj@Q\\GtDD\\ONQFU?WkAeHKw@EuAKcG?kIDuM@oG@uvEJgFJiALo@ZeAVk@\\i@rAeBZm@X{@Hi@Dk@?aAGoAIaAG_@sEdCwBnAmE|BmJlFyCrAo@HuAFkl@o@Ps^|@wr@_F@YEc@[}FmFcEiCq@Wa@CkAViCv@af@hHNk\\","instructions":[{"distance":3313.038,"heading":338.84,"sign":0,"interval":[0,38],"text":"Continue onto Southeast 900 Road","time":397560,"street_name":"Southeast 900 Road"},{"distance":1870.594,"sign":-2,"interval":[38,51],"text":"Turn left onto South 13th Street, MO 13 Business","time":103600,"street_name":"South 13th Street, MO 13 Business"},{"distance":77209.379,"sign":-2,"interval":[51,216],"text":"Turn left onto MO 13","time":2936466,"street_name":"MO 13"},{"distance":190.431,"sign":0,"interval":[216,220],"text":"Continue onto North Kansas Expressway, MO 13","time":19584,"street_name":"North Kansas Expressway, MO 13"},{"distance":3896.719,"sign":-7,"interval":[220,232],"text":"Keep left","time":171505,"street_name":""},{"distance":467.449,"sign":7,"interval":[232,245],"text":"Keep right","time":24039,"street_name":""},{"distance":44.652,"sign":-7,"interval":[245,247],"text":"Keep left","time":2295,"street_name":""},{"distance":1539.639,"sign":-2,"interval":[247,255],"text":"Turn left onto North Glenstone Avenue, MO H","time":88303,"street_name":"North Glenstone Avenue, MO H"},{"distance":1181.371,"sign":2,"interval":[255,257],"text":"Turn right onto East Valley Water Mill Road","time":70879,"street_name":"East Valley Water Mill Road"},{"distance":1344.486,"sign":-2,"interval":[257,267],"text":"Turn left onto North Farm Road 171, 171","time":96801,"street_name":"North Farm Road 171, 171"},{"distance":416.354,"sign":2,"interval":[267,268],"text":"Turn right onto East Farm Road 94","time":29977,"street_name":"East Farm Road 94"},{"distance":0.0,"sign":4,"last_heading":91.48417114853855,"interval":[268,268],"text":"Arrive at destination","time":0,"street_name":""}],"legs":[],"details":{},"ascend":0.0,"descend":0.0,"snapped_waypoints":"mhefFl|fzPnkuByubA"}]}
```
