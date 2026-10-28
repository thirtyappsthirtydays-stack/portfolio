/* Clickable copy of the online consultation booking flow, for the portfolio.
   Nothing is sent, paid or booked. Mounted into a shadow root by index.html. */
(function(){
  var HERO = 'img/5abdb148fa0d8f9c51eb21cff7af9aab.jpg';
  var PHONE = '+90 5XX XXX XX XX';
  var IBAN = 'TR00 0000 0000 0000 0000 0000 00';

  var CSS = [
  ':host{display:block;height:100%;container-type:inline-size;--cream:#F8F6F1;--paper:#FFFFFF;--navy:#1B3A5C;--navy-d:#152843;--ink:#1A2535;--slate:#5A6A7A;--brown:#5A4A35;--brown-d:#3A2D1E;--gold:#C8A96E;--gold-d:#9A7A3A;--gold-t:#7A5A18;--sand:#EDE8DF;--sand-2:#F0EFE9;--line:#DDD6CC;--line-2:#E8E2D8;--sel:#FDF8F0;--red:#C0392B;--ring:#24507E}',
  '*,*::before,*::after{box-sizing:border-box}',
  '.root{position:relative;height:100%;font-family:"DM Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--cream);-webkit-font-smoothing:antialiased}',
  '.app{height:100%;overflow-y:auto;overflow-x:hidden;scroll-behavior:smooth}',
  '@media (prefers-reduced-motion: reduce){.app{scroll-behavior:auto}}',
  'button,input,select,textarea{font:inherit;color:inherit}',
  'button{cursor:pointer}',
  ':focus-visible{outline:2px solid var(--ring);outline-offset:2px}',
  'h1,h2,h3,p{margin:0}',
  '.serif{font-family:"Playfair Display",Georgia,serif}',
  /* header */
  '.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 24px;background:rgba(248,246,241,.96);border-bottom:1px solid var(--line-2);backdrop-filter:blur(8px)}',
  '.brand{display:flex;flex-direction:column;gap:1px;padding:4px 0;border:0;background:none;text-align:left}',
  '.brand b{font-family:"Playfair Display",Georgia,serif;font-size:15px;line-height:20px;font-weight:700;color:var(--navy)}',
  '.brand span{font-size:11px;line-height:14px;letter-spacing:.04em;color:var(--gold-t)}',
  '.lang{display:inline-flex;border-radius:6px;overflow:hidden;background:var(--sand)}',
  '.lang button{min-width:40px;height:32px;padding:0 10px;border:0;background:none;font-size:12px;font-weight:700;color:var(--brown)}',
  '.lang button[aria-pressed="true"]{background:var(--gold);color:var(--navy)}',
  /* stepper */
  '.steps{display:flex;justify-content:center;align-items:center;gap:6px;padding:12px 16px;background:var(--paper);border-bottom:1px solid var(--line-2);flex-wrap:wrap}',
  '.st{display:flex;align-items:center;gap:8px;font-size:12px;line-height:16px;font-weight:500;color:var(--slate)}',
  '.st i{font-style:normal;width:26px;height:26px;border-radius:999px;display:grid;place-items:center;font-size:12px;font-weight:600;background:var(--sand-2);color:var(--slate)}',
  '.st.now{color:var(--navy);font-weight:700}.st.now i{background:var(--navy);color:#fff}',
  '.st.done{color:var(--brown-d)}.st.done i{background:var(--gold);color:var(--navy)}',
  '.st + .st::before{content:"";width:26px;border-top:1px solid #D8DCE6;margin-right:2px}',
  '.bar{height:3px;background:#E4DDD3}.bar span{display:block;height:100%;background:var(--gold);border-radius:0 2px 2px 0;transition:width .5s cubic-bezier(.4,0,.2,1)}',
  /* page */
  '.wrap{max-width:660px;margin:0 auto;padding:20px 24px 96px}',
  '.wide{max-width:980px;margin:0 auto;padding:32px 24px 96px}',
  '.count{display:flex;justify-content:flex-end;padding:18px 24px 0}',
  '.pill{display:inline-flex;align-items:center;height:26px;padding:0 12px;border-radius:100px;background:var(--sand);color:var(--brown-d);font-size:12px;font-weight:700;letter-spacing:.05em}',
  '.back{display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:0 14px;border:1px solid #C8C0B4;border-radius:6px;background:transparent;color:var(--brown-d);font-size:13px;font-weight:600}',
  '.back:hover{background:var(--sand)}',
  '.qn{display:flex;align-items:center;gap:10px;margin:20px 0 16px;font-size:18px;line-height:24px;font-weight:700;color:var(--navy);font-variant-numeric:tabular-nums}.qn span{color:var(--gold-d)}',
  '.q{font-family:"Playfair Display",Georgia,serif;font-size:clamp(24px,5cqi,36px);line-height:1.28;font-weight:600;color:var(--navy);text-wrap:balance}',
  '.q em{font-style:normal;color:var(--red);margin-left:6px}',
  '.q:focus{outline:none}',
  '.sub{margin-top:10px;font-size:14px;line-height:20px;font-weight:500;color:var(--brown)}',
  '.field{margin-top:28px}',
  '.inp{width:100%;padding:8px 0 10px;border:0;border-bottom:2px solid #B9AE9E;background:transparent;font-size:22px;line-height:30px;color:var(--ink);border-radius:0}',
  '.inp::placeholder{color:#9A8F80}',
  '.inp:focus{outline:none;border-bottom-color:var(--gold)}',
  '.inp:focus-visible{outline:none}',
  '.inp.bad{border-bottom-color:var(--red)}',
  'textarea.inp{font-size:18px;line-height:28px;resize:vertical;min-height:110px}',
  '.err{display:flex;align-items:center;gap:6px;margin-top:10px;font-size:13px;font-weight:600;color:var(--red)}',
  '.meta{display:flex;justify-content:flex-end;margin-top:6px;font-size:12px;color:var(--slate);font-variant-numeric:tabular-nums}',
  '.phone{display:flex;gap:14px;align-items:flex-end}',
  '.phone select{flex:none;width:auto;padding:8px 24px 10px 0;border:0;border-bottom:2px solid #B9AE9E;background:transparent;font-size:18px;line-height:30px;appearance:none;-webkit-appearance:none;background-image:linear-gradient(45deg,transparent 50%,#5A4A35 50%),linear-gradient(135deg,#5A4A35 50%,transparent 50%);background-position:calc(100% - 9px) 55%,calc(100% - 4px) 55%;background-size:5px 5px;background-repeat:no-repeat;border-radius:0}',
  '.phone select:focus{outline:none;border-bottom-color:var(--gold)}',
  '.phone .inp{flex:1;min-width:0}',
  '.check{display:flex;align-items:flex-start;gap:10px;margin-top:18px;font-size:14px;line-height:20px;color:var(--brown-d);cursor:pointer}',
  '.check input{width:18px;height:18px;margin:1px 0 0;accent-color:var(--navy)}',
  '.choices{display:flex;flex-direction:column;gap:9px;margin-top:22px}',
  '.ch{display:flex;align-items:center;gap:14px;width:100%;min-height:48px;padding:12px 18px;border:1.5px solid var(--line);border-radius:10px;background:var(--paper);font-size:15px;line-height:20px;text-align:left;transition:background-color .15s,border-color .15s}',
  '.ch:hover{border-color:var(--gold);background:var(--sel)}',
  '.ch[aria-pressed="true"]{border-color:var(--gold);background:var(--sel)}',
  '.key{flex:none;width:24px;height:24px;border-radius:5px;border:1.5px solid #8A7A65;display:grid;place-items:center;font-size:10px;font-weight:700;color:var(--brown)}',
  '.ch[aria-pressed="true"] .key{background:var(--gold);border-color:var(--gold);color:var(--navy)}',
  '.yn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:24px}',
  '.ynb{display:flex;flex-direction:column;align-items:center;gap:6px;min-height:120px;justify-content:center;border:1.5px solid var(--line);border-radius:12px;background:var(--paper);font-size:17px;font-weight:600;color:var(--navy)}',
  '.ynb small{font-size:11px;font-weight:600;color:var(--slate)}',
  '.ynb:hover,.ynb[aria-pressed="true"]{border-color:var(--gold);background:var(--sel)}',
  '.ynb svg{width:22px;height:22px}',
  '.actions{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:28px}',
  '.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:0 24px;border:0;border-radius:8px;background:var(--navy);color:#fff;font-size:15px;font-weight:600;transition:background-color .15s}',
  '.btn:hover{background:var(--navy-d)}',
  '.btn[disabled]{background:#A7B0BE;cursor:default}',
  '.btn.pay{background:var(--gold);color:var(--navy)}.btn.pay:hover{background:#BE9C5C}',
  '.btn.ghost{background:var(--paper);color:var(--navy);border:1px solid var(--line)}.btn.ghost:hover{background:var(--sel)}',
  '.hint{font-size:12px;font-weight:500;color:var(--brown)}',
  '.dots{display:flex;justify-content:center;gap:6px;margin-top:40px}',
  '.dots span{width:16px;height:3px;border-radius:2px;background:#D9D3C9}.dots .d{background:#E2CFA3}.dots .c{width:28px;background:var(--gold)}',
  /* intro */
  '.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:center}',
  '.hero img{display:block;width:100%;height:auto;border-radius:14px;box-shadow:0 12px 32px rgba(27,58,92,.16)}',
  '.h1{font-family:"Playfair Display",Georgia,serif;font-size:clamp(28px,4.2cqi,40px);line-height:1.16;font-weight:700;color:var(--navy);text-wrap:balance}',
  '.lead{margin-top:14px;font-size:16px;line-height:24px;color:var(--slate)}',
  '.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:40px}',
  '.card{display:flex;flex-direction:column;gap:10px;padding:22px;border:1px solid var(--line-2);border-radius:14px;background:var(--paper)}',
  '.card.first{border-color:var(--gold)}',
  '.card .n{font-family:"Playfair Display",Georgia,serif;font-size:40px;line-height:44px;font-weight:700;color:var(--gold-d)}',
  '.card h3{font-size:16px;line-height:22px;font-weight:700;color:var(--navy)}',
  '.card p{font-size:14px;line-height:22px;color:var(--slate)}',
  '.link{align-self:flex-start;margin-top:auto;padding:4px 0;border:0;background:none;font-size:14px;font-weight:700;color:var(--gold-t)}',
  '.link:hover{text-decoration:underline;text-underline-offset:3px}',
  '.alt{margin-top:28px;text-align:center;font-size:15px;line-height:22px;color:var(--brown-d)}.alt b{color:var(--navy)}',
  '.quote{margin-top:32px;padding:32px 36px;border-radius:16px;background:var(--navy);color:#fff}',
  '.quote .mk{font-family:"Playfair Display",Georgia,serif;font-size:40px;line-height:20px;color:var(--gold)}',
  '.quote p{margin-top:18px;font-size:18px;line-height:30px}',
  '.quote cite{display:block;margin-top:18px;font-style:normal;font-size:14px;font-weight:700;color:#D4B97A}',
  '.rating{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:28px;font-size:14px;color:var(--slate)}.rating b{color:var(--navy)}',
  '.stars{color:#E0A91B;letter-spacing:2px}',
  /* payment */
  '.fee{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-top:24px;padding:22px 24px;border-radius:12px;background:var(--navy);color:#fff}',
  '.fee small{display:block;font-size:13px;line-height:18px;color:#DCE4EE}',
  '.fee b{display:block;margin-top:4px;font-family:"Playfair Display",Georgia,serif;font-size:34px;line-height:40px;font-weight:700;color:#E7CF98}',
  '.fee span{font-family:"Playfair Display",Georgia,serif;font-size:20px;font-weight:700;color:#D4B97A}',
  '.incl{margin-top:14px;font-size:14px;line-height:22px;color:var(--brown-d)}',
  '.rows{margin-top:18px;border-top:1px solid var(--line-2)}',
  '.row{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--line-2);font-size:14px}',
  '.row span{color:var(--slate)}.row b{text-align:right;color:var(--navy);font-variant-numeric:tabular-nums;overflow-wrap:anywhere}',
  '.copy{margin-left:10px;padding:4px 10px;border:1px solid var(--line);border-radius:6px;background:var(--paper);font-size:12px;font-weight:600;color:var(--brown-d)}',
  '.fine{margin-top:10px;font-size:12px;color:var(--slate)}',
  '.notice{display:flex;gap:10px;align-items:flex-start;margin-top:22px;padding:14px 16px;border:1px solid #E7D3A6;border-radius:10px;background:#FDF8EC;font-size:14px;line-height:21px;color:var(--brown-d)}',
  '.notice.go{border-color:#BFE0C8;background:#EEF7F0}',
  '.notice svg{flex:none;width:18px;height:18px;margin-top:2px}',
  /* language */
  '.lopt{display:flex;align-items:center;gap:16px;width:100%;padding:16px 18px;border:1.5px solid var(--line);border-radius:12px;background:var(--paper);text-align:left}',
  '.lopt:hover,.lopt[aria-pressed="true"]{border-color:var(--gold);background:var(--sel)}',
  '.badge{flex:none;width:40px;height:40px;border-radius:8px;display:grid;place-items:center;background:var(--sand);color:var(--navy);font-size:13px;font-weight:700}',
  '.lopt[aria-pressed="true"] .badge{background:var(--navy);color:#fff}',
  '.lopt b{display:block;font-size:17px;color:var(--navy)}.lopt small{font-size:13px;color:var(--slate)}',
  /* calendar */
  '.cal{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;margin-top:24px;padding:22px;border:1px solid var(--line-2);border-radius:14px;background:var(--paper)}',
  '.mhead{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}',
  '.mhead b{font-size:16px;color:var(--navy)}',
  '.nav{width:34px;height:34px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--navy);font-size:16px}',
  '.nav[disabled]{opacity:.35;cursor:default}',
  '.grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;text-align:center}',
  '.grid .wd{padding:4px 0;font-size:11px;font-weight:700;letter-spacing:.04em;color:var(--slate)}',
  '.day{aspect-ratio:1;max-height:44px;border:0;border-radius:8px;background:none;font-size:14px;font-variant-numeric:tabular-nums;color:#A9A398;text-decoration:line-through;cursor:default}',
  '.day.ok{background:var(--sel);color:var(--gold-t);font-weight:600;text-decoration:none;cursor:pointer}',
  '.day.ok:hover{background:#F4E9D2}',
  '.day.today{outline:1px solid #C8C0B4;outline-offset:-1px;text-decoration:none;color:var(--ink)}',
  '.day[aria-pressed="true"]{background:var(--navy);color:#fff}',
  '.slots h4{margin:0 0 12px;font-size:14px;color:var(--navy)}',
  '.slots .list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}',
  '.slot{min-height:44px;border:1px solid var(--line);border-radius:8px;background:var(--paper);font-size:15px;font-weight:600;color:var(--navy);font-variant-numeric:tabular-nums}',
  '.slot:hover{border-color:var(--gold);color:var(--gold-t)}',
  '.slot[aria-pressed="true"]{background:var(--navy);border-color:var(--navy);color:#fff}',
  '.empty{font-size:14px;line-height:21px;color:var(--slate)}',
  '.tz{margin-top:10px;font-size:13px;color:var(--slate)}',
  /* done */
  '.ok-mark{width:52px;height:52px;border-radius:999px;display:grid;place-items:center;background:var(--gold);color:var(--navy)}',
  '.sum{margin-top:22px;padding:6px 20px;border:1px solid var(--line-2);border-radius:12px;background:var(--paper)}',
  '.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}',
  '.chips span{padding:5px 12px;border-radius:999px;background:var(--sand);font-size:13px;font-weight:600;color:var(--brown-d)}',
  '.tips{margin-top:22px;padding:18px 20px;border-radius:12px;background:#EEF3F9}',
  '.tips h3{font-size:15px;color:var(--navy)}',
  '.tips li{margin-top:10px;font-size:14px;line-height:21px;color:var(--ink)}',
  '.tips ul{margin:0;padding-left:18px}',
  '.sandbox{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:28px;padding:14px 16px;border:1px dashed #B9AE9E;border-radius:10px;font-size:13px;line-height:19px;color:var(--brown-d)}',
  /* floating + overlays */
  '.wa{position:absolute;right:18px;bottom:18px;z-index:6;display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 18px;border:0;border-radius:999px;background:#25D366;color:#0B3D1E;font-size:14px;font-weight:700;box-shadow:0 6px 18px rgba(11,61,30,.28)}',
  '.wa svg{width:16px;height:16px}',
  '.toast{position:absolute;left:50%;bottom:76px;z-index:8;max-width:min(420px,calc(100% - 32px));padding:12px 16px;border-radius:10px;background:var(--ink);color:#fff;font-size:13px;line-height:19px;transform:translate(-50%,8px);opacity:0;pointer-events:none;transition:opacity .2s,transform .2s}',
  '.toast.on{opacity:1;transform:translate(-50%,0)}',
  '.dlg{position:absolute;inset:0;z-index:9;display:grid;place-items:center;padding:20px;background:rgba(26,37,53,.55)}',
  '.dlg .box{width:100%;max-width:440px;padding:26px;border-radius:14px;background:var(--paper);box-shadow:0 24px 60px rgba(0,0,0,.25)}',
  '.dlg h2{font-family:"Playfair Display",Georgia,serif;font-size:22px;line-height:28px;color:var(--navy)}',
  '.dlg p{margin-top:10px;font-size:14px;line-height:21px;color:var(--slate)}',
  '.dlg .actions{margin-top:20px}',
  '.dlg .actions .btn{flex:1}',
  /* narrow frame */
  '@container (max-width: 700px){',
  '.top{padding:10px 16px}.brand b{font-size:14px}',
  '.st b{display:none}.st + .st::before{width:14px}',
  '.wrap{padding:16px 18px 96px}.wide{padding:20px 18px 96px}.count{padding:14px 18px 0}',
  '.hero{grid-template-columns:minmax(0,1fr);gap:22px}',
  '.cards{grid-template-columns:minmax(0,1fr);gap:12px;margin-top:26px}',
  '.card{padding:18px}.card .n{font-size:32px;line-height:36px}',
  '.quote{padding:24px 22px}.quote p{font-size:16px;line-height:26px}',
  '.cal{grid-template-columns:minmax(0,1fr);padding:16px}',
  '.inp{font-size:20px}.phone select{font-size:16px}',
  '.fee b{font-size:30px}',
  '.wa span{display:none}.wa{width:48px;padding:0;justify-content:center}',
  '}'
  ].join('\n');

  var COUNTRIES = [['+90','Türkiye','Türkiye'],['+49','Germany','Almanya'],['+44','United Kingdom','Birleşik Krallık'],['+1','United States','ABD'],['+31','Netherlands','Hollanda'],['+33','France','Fransa'],['+994','Azerbaijan','Azerbaycan']];
  var REASONS = {
    en:['Lung Cancer','Suspected Lung Nodule','Bronchiectasis','Thymoma','Mediastinal Tumor or Cyst','Pectus Excavatum','Pneumothorax','Congenital Lung Cyst in Infant','Mesothelioma','Post-Surgery Follow-up','Other'],
    tr:['Akciğer Kanseri','Akciğerde Nodül Şüphesi','Bronşektazi','Timoma','Mediastinal Tümör veya Kist','Pektus Ekskavatum (Göğüs Çökmesi)','Pnömotoraks (Akciğer Sönmesi)','Bebeklerde Doğumsal Akciğer Kisti','Mezotelyoma','Ameliyat Sonrası Takip','Diğer']
  };
  var T = {
    en:{spec:'Lung Surgery Specialist', steps:['Details','Payment','Language','Appointment'], of:function(a,b){return a+' of '+b;}, back:'Back', cont:'Continue', enter:'or press Enter ↵', req:'Required',
      title:'Online Medical Assessment with Prof. Dr. Semih Halezeroğlu', sub:'Three stages, from booking to your consultation.', go:'Go to Form',
      c1h:'Fill the Form & Book Your Appointment', c1p:'Enter the patient\'s details, complete the payment, and select a convenient appointment time.',
      c2h:'Document Review', c2p:'Your medical records on E-Nabız, imaging studies, lab results, and any documents you share will be thoroughly reviewed by Prof. Dr. Semih Halezeroğlu.',
      c3h:'Consultation', c3p:'At the scheduled time, Prof. Dr. Semih Halezeroğlu will call you via WhatsApp video. The consultation lasts 30 minutes.',
      alt:'Alternatively, you may reach our assistant by call or WhatsApp at',
      quote:'In healthcare, especially in situations requiring surgical intervention, the decisions made are vital. In critical processes such as lung diseases and cancer, seeking a second expert opinion can fundamentally change a patient\'s treatment journey.',
      reviews:'40 Google reviews',
      q1:'What is the patient\'s full name?', q1s:'If you\'re booking for someone else, enter their name.', q1p:'Full name...', q1e:'Please enter both first and last name',
      q2:'How old is the patient?', q2p:'Age', q2e:'Please enter an age between 0 and 120',
      q3:'Which WhatsApp number should the doctor call?', q3s:'The doctor calls the patient on WhatsApp video at the booked time.', q3p:'Phone number', q3c:'The patient doesn\'t use WhatsApp, Google Meet is fine', q3e:'Please enter a phone number with at least 7 digits',
      q4:'What is the reason for the consultation?', q4s:'(You can select more than one)', q4e:'Please choose at least one',
      q5:'Has the patient had chest surgery before?', yes:'Yes', no:'No', pressY:'Press Y', pressN:'Press N', ky:'y', kn:'n', q5e:'Please choose Yes or No',
      q6:'Briefly describe the patient\'s situation', q6s:'Optional. It helps the doctor prepare.', q6p:'Current diagnosis, treatment, or questions for the doctor...',
      payH:'Complete the payment', payS:'Send the fee by bank transfer, then continue to choose a language and a time.', fee:'Online Medical Consultation (20–30 min)',
      incl:'Includes a review of the records you send, and a video call with Prof. Dr. Semih Halezeroğlu.', bank:'Bank', ref:'Reference', refE:'Please enter the patient\'s name', copy:'Copy', masked:'IBAN masked for this portfolio.',
      sent:'I\'ve sent the transfer', dlgH:'Have you sent the bank transfer?', dlgP:'Please don\'t book before completing the payment. Continue only after you\'ve sent the transfer.', dlgY:'Yes, I\'ve sent it', dlgN:'Go back',
      lgH:'Which language should your emails be in?', lgS:'Confirmation and reminder emails will be sent in this language.',
      apH:'Choose a time', apN:'<b>Before you book:</b> pick a time at least 24 hours ahead, so the doctor can review your documents.', tz:'Times are in Istanbul time (GMT+3).', pick:'Pick a day to see open times.', none:'No open times this day.', slotsFor:'Open times', book:'Confirm booking',
      months:['January','February','March','April','May','June','July','August','September','October','November','December'], wd:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], days:['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
      doneH:'Your appointment is booked', doneS:'A confirmation email is on its way.', sPatient:'Patient', sWhen:'Date and time', sCall:'Call on', sLang:'Email language', wa:'WhatsApp video', meet:'Google Meet',
      now:'<b>What to do now:</b> send a WhatsApp message saying “I have booked my appointment”.', msg:'Message on WhatsApp', send:'Then send the records you have:', recs:['E-Nabız','CT','PET-CT','Lab results','Pathology'],
      prepH:'What to do before the consultation?', prep1:'Note down the questions you want to ask the doctor.', prep2wa:'Keep the phone nearby at the booked time. The doctor calls on WhatsApp video.', prep2meet:'Keep the device you\'ll use for Google Meet nearby at the booked time.',
      contact:'Questions? Call or WhatsApp our assistant at'},
    tr:{spec:'Göğüs Cerrahisi Uzmanı', steps:['Bilgiler','Ödeme','Dil','Randevu'], of:function(a,b){return a+' / '+b;}, back:'Geri', cont:'Devam', enter:'ya da Enter ↵', req:'Zorunlu',
      title:'Prof. Dr. Semih Halezeroğlu ile Online Tıbbi Değerlendirme', sub:'Randevudan görüşmeye üç aşama.', go:'Forma Git',
      c1h:'Formu Doldurun ve Randevunuzu Alın', c1p:'Hastanın bilgilerini girin, ödemeyi tamamlayın ve size uygun bir randevu saati seçin.',
      c2h:'Belge İncelemesi', c2p:'E-Nabız’daki tıbbi kayıtlarınız, görüntülemeleriniz, tahlil sonuçlarınız ve paylaştığınız tüm belgeler Prof. Dr. Semih Halezeroğlu tarafından ayrıntılı olarak incelenir.',
      c3h:'Görüşme', c3p:'Randevu saatinde Prof. Dr. Semih Halezeroğlu sizi WhatsApp üzerinden görüntülü arar. Görüşme 30 dakika sürer.',
      alt:'Dilerseniz asistanımıza telefonla ya da WhatsApp’tan da ulaşabilirsiniz:',
      quote:'Sağlıkta, özellikle cerrahi müdahale gerektiren durumlarda verilen kararlar hayati önem taşır. Akciğer hastalıkları ve kanser gibi kritik süreçlerde ikinci bir uzman görüşü almak, hastanın tedavi yolculuğunu kökten değiştirebilir.',
      reviews:'40 Google yorumu',
      q1:'Hastanın adı ve soyadı nedir?', q1s:'Başkası için randevu alıyorsanız onun adını yazın.', q1p:'Ad soyad...', q1e:'Lütfen hem adı hem soyadı girin',
      q2:'Hasta kaç yaşında?', q2p:'Yaş', q2e:'Lütfen 0 ile 120 arasında bir yaş girin',
      q3:'Doktor hangi WhatsApp numarasını arasın?', q3s:'Doktor, randevu saatinde hastayı WhatsApp’tan görüntülü arar.', q3p:'Telefon numarası', q3c:'Hasta WhatsApp kullanmıyor, Google Meet olur', q3e:'Lütfen en az 7 haneli bir telefon numarası girin',
      q4:'Görüşmenin nedeni nedir?', q4s:'(Birden fazla seçebilirsiniz)', q4e:'Lütfen en az birini seçin',
      q5:'Hasta daha önce göğüs ameliyatı oldu mu?', yes:'Evet', no:'Hayır', pressY:'E’ye basın', pressN:'H’ye basın', ky:'e', kn:'h', q5e:'Lütfen Evet ya da Hayır’ı seçin',
      q6:'Hastanın durumunu kısaca anlatın', q6s:'İsteğe bağlı. Doktorun hazırlanmasına yardımcı olur.', q6p:'Mevcut tanı, tedavi ya da doktora sormak istedikleriniz...',
      payH:'Ödemeyi tamamlayın', payS:'Ücreti banka havalesiyle gönderin, ardından dil ve saat seçimine geçin.', fee:'Online Tıbbi Görüşme (20–30 dk)',
      incl:'Gönderdiğiniz kayıtların incelenmesini ve Prof. Dr. Semih Halezeroğlu ile görüntülü görüşmeyi kapsar.', bank:'Banka', ref:'Açıklama', refE:'Lütfen hastanın adını yazın', copy:'Kopyala', masked:'IBAN masked for this portfolio.',
      sent:'Havaleyi gönderdim', dlgH:'Banka havalesini gönderdiniz mi?', dlgP:'Lütfen ödemeyi tamamlamadan randevu almayın. Havaleyi gönderdikten sonra devam edin.', dlgY:'Evet, gönderdim', dlgN:'Geri dön',
      lgH:'E-postalarınız hangi dilde olsun?', lgS:'Onay ve hatırlatma e-postaları bu dilde gönderilir.',
      apH:'Bir saat seçin', apN:'<b>Randevu almadan önce:</b> doktorun belgelerinizi inceleyebilmesi için en az 24 saat sonrasına bir saat seçin.', tz:'Saatler İstanbul saatine göredir (GMT+3).', pick:'Açık saatleri görmek için bir gün seçin.', none:'Bu gün için açık saat yok.', slotsFor:'Açık saatler', book:'Randevuyu onayla',
      months:['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'], wd:['Pzt','Sal','Çar','Per','Cum','Cmt','Paz'], days:['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'],
      doneH:'Randevunuz alındı', doneS:'Onay e-postası yolda.', sPatient:'Hasta', sWhen:'Tarih ve saat', sCall:'Görüşme', sLang:'E-posta dili', wa:'WhatsApp görüntülü', meet:'Google Meet',
      now:'<b>Şimdi ne yapmalı:</b> WhatsApp’tan “Randevumu aldım” yazan bir mesaj gönderin.', msg:'WhatsApp’tan yaz', send:'Ardından elinizdeki kayıtları gönderin:', recs:['E-Nabız','BT','PET-BT','Tahlil sonuçları','Patoloji'],
      prepH:'Görüşmeden önce ne yapmalı?', prep1:'Doktora sormak istediğiniz soruları not edin.', prep2wa:'Randevu saatinde telefonu yanınızda bulundurun. Doktor WhatsApp’tan görüntülü arar.', prep2meet:'Randevu saatinde Google Meet için kullanacağınız cihazı yanınızda bulundurun.',
      contact:'Sorularınız için asistanımızı arayın ya da WhatsApp’tan yazın:'}
  };

  var ICON = {
    arrow:'<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
    down:'<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3v10M4 9l4 4 4-4"/></svg>',
    check:'<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.2 5 8.6l4.5-5"/></svg>',
    x:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    tick:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg>',
    big:'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg>',
    cal:'<svg viewBox="0 0 24 24" fill="none" stroke="#9A7A3A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
    chat:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/></svg>',
    info:'<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="8" cy="8" r="6.5"/><path d="M8 7v4M8 4.8v.2" stroke-linecap="round"/></svg>'
  };

  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function pad(n){ return (n < 10 ? '0' : '') + n; }

  function mount(host){
    var sr = host.shadowRoot || host.attachShadow({mode:'open'});
    sr.innerHTML = '<style>' + CSS + '</style><div class="root"><div class="app" tabindex="-1"></div>' +
      '<button type="button" class="wa" data-act="wa" aria-label="WhatsApp">' + ICON.chat + '<span>WhatsApp</span></button>' +
      '<div class="toast" role="status" aria-live="polite"></div><div class="dlg-slot"></div></div>';
    var app = sr.querySelector('.app'), toastEl = sr.querySelector('.toast'), dlgSlot = sr.querySelector('.dlg-slot');
    var S, toastT;
    function fresh(){
      var keepLang = S ? S.lang : 'en';
      S = {lang:keepLang, screen:'intro', q:0, err:'', dlg:false, d:{name:'', age:'', cc:'+90', phone:'', meet:false, reasons:[], surgery:null, desc:'', mail:null, day:null, slot:null}, month:0};
    }
    function t(k){ return T[S.lang][k]; }
    function toast(msg){
      toastEl.textContent = msg; toastEl.classList.add('on');
      clearTimeout(toastT); toastT = setTimeout(function(){ toastEl.classList.remove('on'); }, 2800);
    }

    /* ---- calendar helpers: real dates, Istanbul working days, 24h notice ---- */
    function today(){ var n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); }
    function key(dt){ return dt.getFullYear() + '-' + pad(dt.getMonth() + 1) + '-' + pad(dt.getDate()); }
    function hash(s){ var h = 0; for(var i = 0; i < s.length; i++){ h = (h * 31 + s.charCodeAt(i)) >>> 0; } return h; }
    function openDay(dt){
      var dow = dt.getDay(); if(dow === 0 || dow === 6) return false;
      var min = today(); min.setDate(min.getDate() + 2); if(dt < min) return false;
      return hash(key(dt)) % 5 !== 0;
    }
    function slotsFor(dt){
      var all = ['10:00','11:00','12:00','14:00','15:00','16:30'], h = hash(key(dt) + 's');
      return all.filter(function(s, i){ return ((h >> i) & 3) !== 0; });
    }

    /* ---- views ---- */
    function header(){
      return '<header class="top"><button type="button" class="brand" data-act="home" aria-label="Prof. Dr. Semih Halezeroğlu, back to the start"><b>Prof. Dr. Semih Halezeroğlu</b><span>' + esc(t('spec')) + '</span></button>' +
        '<div class="lang" role="group" aria-label="Language"><button type="button" data-act="lang" data-v="tr" aria-pressed="' + (S.lang === 'tr') + '">TR</button><button type="button" data-act="lang" data-v="en" aria-pressed="' + (S.lang === 'en') + '">EN</button></div></header>';
    }
    function stepper(cur, bar){
      var names = t('steps');
      return '<nav class="steps" aria-label="Booking steps">' + names.map(function(n, i){
        var cls = i < cur ? 'done' : (i === cur ? 'now' : '');
        return '<span class="st ' + cls + '"' + (i === cur ? ' aria-current="step"' : '') + '><i>' + (i < cur ? ICON.check : (i + 1)) + '</i><b>' + esc(n) + '</b></span>';
      }).join('') + '</nav><div class="bar"><span style="width:' + Math.round(bar * 100) + '%"></span></div>';
    }
    function backBtn(){ return '<button type="button" class="back" data-act="back">‹ ' + esc(t('back')) + '</button>'; }
    function errLine(){ return S.err ? '<p class="err" role="alert">' + ICON.info + esc(S.err) + '</p>' : ''; }
    function contBtn(label, extra){
      return '<div class="actions"><button type="button" class="btn" data-act="next"' + (extra || '') + '>' + esc(label || t('cont')) + ' ' + ICON.down + '</button><span class="hint">' + esc(t('enter')) + '</span></div>';
    }

    function vIntro(){
      return header() + '<main class="wide">' +
        '<section class="hero"><img src="' + HERO + '" alt="Prof. Dr. Semih Halezeroğlu at his desk reviewing lung scans, and a family on a video consultation at home" width="1200" height="660"><div>' +
        '<h1 class="h1" tabindex="-1">' + esc(t('title')) + '</h1><p class="lead">' + esc(t('sub')) + '</p>' +
        '<div class="actions"><button type="button" class="btn" data-act="start">' + esc(t('go')) + ' ' + ICON.arrow + '</button></div></div></section>' +
        '<section class="cards">' +
          '<div class="card first"><span class="n">1</span><h3>' + esc(t('c1h')) + '</h3><p>' + esc(t('c1p')) + '</p><button type="button" class="link" data-act="start">' + esc(t('go')) + ' →</button></div>' +
          '<div class="card"><span class="n">2</span><h3>' + esc(t('c2h')) + '</h3><p>' + esc(t('c2p')) + '</p></div>' +
          '<div class="card"><span class="n">3</span><h3>' + esc(t('c3h')) + '</h3><p>' + esc(t('c3p')) + '</p></div>' +
        '</section>' +
        '<p class="alt">' + esc(t('alt')) + ' <b>' + PHONE + '</b>.</p>' +
        '<blockquote class="quote" style="margin-inline:0"><span class="mk" aria-hidden="true">“</span><p>' + esc(t('quote')) + '</p><cite>— Prof. Dr. Semih Halezeroğlu</cite></blockquote>' +
        '<p class="rating"><b>Prof. Dr. Semih Halezeroğlu</b><span class="stars" aria-hidden="true">★★★★★</span><span>' + esc(t('reviews')) + '</span></p>' +
        '</main>';
    }

    function qWrap(i, body, opts){
      opts = opts || {};
      var dots = ''; for(var k = 0; k < 6; k++){ dots += '<span class="' + (k < i ? 'd' : (k === i ? 'c' : '')) + '"></span>'; }
      return header() + stepper(0, i / 6) +
        '<div class="count"><span class="pill">' + esc(t('of')(i + 1, 6)) + '</span></div>' +
        '<main class="wrap">' + backBtn() +
        '<p class="qn" aria-hidden="true">' + pad(i + 1) + ' <span>→</span></p>' +
        '<h1 class="q" id="q" tabindex="-1">' + esc(opts.q) + (opts.req === false ? '' : '<em aria-hidden="true">*</em><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)"> (' + esc(t('req')) + ')</span>') + '</h1>' +
        (opts.sub ? '<p class="sub">' + esc(opts.sub) + '</p>' : '') +
        body + '<div class="dots" aria-hidden="true">' + dots + '</div></main>';
    }
    function vQ(){
      var d = S.d, i = S.q, body = '';
      if(i === 0){
        body = '<div class="field"><input class="inp' + (S.err ? ' bad' : '') + '" id="f" type="text" autocomplete="name" aria-labelledby="q" aria-invalid="' + !!S.err + '" placeholder="' + esc(t('q1p')) + '" value="' + esc(d.name) + '">' + errLine() + '</div>' + contBtn();
        return qWrap(i, body, {q:t('q1'), sub:t('q1s')});
      }
      if(i === 1){
        body = '<div class="field" style="max-width:220px"><input class="inp' + (S.err ? ' bad' : '') + '" id="f" type="number" inputmode="numeric" min="0" max="120" aria-labelledby="q" aria-invalid="' + !!S.err + '" placeholder="' + esc(t('q2p')) + '" value="' + esc(d.age) + '"></div>' + errLine() + contBtn();
        return qWrap(i, body, {q:t('q2')});
      }
      if(i === 2){
        var opts = COUNTRIES.map(function(c){ return '<option value="' + c[0] + '"' + (c[0] === d.cc ? ' selected' : '') + '>' + c[0] + ' ' + esc(S.lang === 'tr' ? c[2] : c[1]) + '</option>'; }).join('');
        body = '<div class="field"><div class="phone"><select id="cc" aria-label="Country code">' + opts + '</select>' +
          '<input class="inp' + (S.err ? ' bad' : '') + '" id="f" type="tel" autocomplete="tel-national" aria-labelledby="q" aria-invalid="' + !!S.err + '" placeholder="' + esc(t('q3p')) + '" value="' + esc(d.phone) + '"></div>' +
          '<label class="check"><input type="checkbox" id="meet"' + (d.meet ? ' checked' : '') + '><span>' + esc(t('q3c')) + '</span></label>' + errLine() + '</div>' + contBtn();
        return qWrap(i, body, {q:t('q3'), sub:t('q3s')});
      }
      if(i === 3){
        body = '<div class="choices" role="group" aria-labelledby="q">' + REASONS[S.lang].map(function(r, k){
          var on = d.reasons.indexOf(k) > -1, L = String.fromCharCode(65 + k);
          return '<button type="button" class="ch" data-act="reason" data-v="' + k + '" aria-pressed="' + on + '"><span class="key" aria-hidden="true">' + (on ? ICON.check : L) + '</span><span>' + esc(r) + '</span></button>';
        }).join('') + '</div>' + errLine() + contBtn();
        return qWrap(i, body, {q:t('q4'), sub:t('q4s')});
      }
      if(i === 4){
        body = '<div class="yn" role="group" aria-labelledby="q">' +
          '<button type="button" class="ynb" data-act="yn" data-v="1" aria-pressed="' + (d.surgery === true) + '">' + ICON.tick + esc(t('yes')) + '<small aria-hidden="true">' + esc(t('pressY')) + '</small></button>' +
          '<button type="button" class="ynb" data-act="yn" data-v="0" aria-pressed="' + (d.surgery === false) + '">' + ICON.x + esc(t('no')) + '<small aria-hidden="true">' + esc(t('pressN')) + '</small></button></div>' + errLine() + contBtn();
        return qWrap(i, body, {q:t('q5')});
      }
      body = '<div class="field"><textarea class="inp" id="f" maxlength="500" rows="4" aria-labelledby="q" placeholder="' + esc(t('q6p')) + '">' + esc(d.desc) + '</textarea><p class="meta"><span id="n">' + d.desc.length + '</span>&nbsp;/ 500</p></div>' +
        '<div class="actions"><button type="button" class="btn" data-act="next">' + esc(t('cont')) + ' ' + ICON.down + '</button><span class="hint">' + (S.lang === 'tr' ? 'ya da Ctrl + Enter' : 'or Ctrl + Enter') + '</span></div>';
      return qWrap(i, body, {q:t('q6'), sub:t('q6s'), req:false});
    }

    function vPay(){
      var ref = S.d.name.trim();
      return header() + stepper(1, 1) + '<main class="wrap" style="padding-top:28px">' + backBtn() +
        '<h1 class="q" tabindex="-1" style="margin-top:22px">' + esc(t('payH')) + '</h1><p class="sub">' + esc(t('payS')) + '</p>' +
        '<div class="fee"><div><small>' + esc(t('fee')) + '</small><b>€300</b></div><span>₺15.000</span></div>' +
        '<p class="incl">' + esc(t('incl')) + '</p>' +
        '<div class="rows"><div class="row"><span>' + esc(t('bank')) + '</span><b>İş Bankası</b></div>' +
        '<div class="row"><span>IBAN</span><b>' + IBAN + '<button type="button" class="copy" data-act="copy">' + esc(t('copy')) + '</button></b></div>' +
        '<div class="row"><span>' + esc(t('ref')) + '</span><b>' + esc(ref || t('refE')) + '</b></div></div>' +
        '<p class="fine">' + esc(t('masked')) + '</p>' +
        '<div class="actions"><button type="button" class="btn pay" data-act="paid">' + esc(t('sent')) + ' ' + ICON.arrow + '</button></div></main>';
    }
    function vDlg(){
      return '<div class="dlg"><div class="box" role="dialog" aria-modal="true" aria-labelledby="dh" aria-describedby="dp"><h2 id="dh">' + esc(t('dlgH')) + '</h2><p id="dp">' + esc(t('dlgP')) + '</p>' +
        '<div class="actions"><button type="button" class="btn pay" data-act="dlg-yes">' + esc(t('dlgY')) + ' ' + ICON.arrow + '</button><button type="button" class="btn ghost" data-act="dlg-no">← ' + esc(t('dlgN')) + '</button></div></div></div>';
    }
    function vLang(){
      var m = S.d.mail;
      return header() + stepper(2, 1) + '<main class="wrap" style="padding-top:28px">' + backBtn() +
        '<h1 class="q" id="q" tabindex="-1" style="margin-top:22px">' + esc(t('lgH')) + '<em aria-hidden="true">*</em></h1><p class="sub">' + esc(t('lgS')) + '</p>' +
        '<div class="choices" role="group" aria-labelledby="q">' +
          '<button type="button" class="lopt" data-act="mail" data-v="tr" aria-pressed="' + (m === 'tr') + '"><span class="badge" aria-hidden="true">TR</span><span><b>Türkçe</b><small>Tüm e-postalar Türkçe gönderilir</small></span></button>' +
          '<button type="button" class="lopt" data-act="mail" data-v="en" aria-pressed="' + (m === 'en') + '"><span class="badge" aria-hidden="true">EN</span><span><b>English</b><small>All emails sent in English</small></span></button>' +
        '</div>' + errLine() + contBtn() + '</main>';
    }
    function vAppt(){
      var base = today(), first = new Date(base.getFullYear(), base.getMonth() + S.month, 1);
      var y = first.getFullYear(), mo = first.getMonth(), daysIn = new Date(y, mo + 1, 0).getDate(), lead = (first.getDay() + 6) % 7;
      var cells = t('wd').map(function(w){ return '<span class="wd">' + esc(w) + '</span>'; }).join('');
      for(var b = 0; b < lead; b++) cells += '<span></span>';
      for(var dd = 1; dd <= daysIn; dd++){
        var dt = new Date(y, mo, dd), k = key(dt), ok = openDay(dt), isT = k === key(base), sel = S.d.day === k;
        cells += '<button type="button" class="day' + (ok ? ' ok' : '') + (isT ? ' today' : '') + '"' + (ok ? ' data-act="day" data-v="' + k + '"' : ' disabled') +
          ' aria-pressed="' + sel + '" aria-label="' + dd + ' ' + esc(t('months')[mo]) + '">' + dd + '</button>';
      }
      var slots;
      if(!S.d.day){ slots = '<p class="empty">' + esc(t('pick')) + '</p>'; }
      else {
        var p = S.d.day.split('-'), sd = new Date(+p[0], +p[1] - 1, +p[2]), list = slotsFor(sd);
        slots = '<h4>' + esc(t('days')[sd.getDay()] + ', ' + sd.getDate() + ' ' + t('months')[sd.getMonth()]) + '</h4>' +
          (list.length ? '<div class="list" role="group" aria-label="' + esc(t('slotsFor')) + '">' + list.map(function(s){ return '<button type="button" class="slot" data-act="slot" data-v="' + s + '" aria-pressed="' + (S.d.slot === s) + '">' + s + '</button>'; }).join('') + '</div>' : '<p class="empty">' + esc(t('none')) + '</p>');
      }
      return header() + stepper(3, 1) + '<main class="wrap" style="max-width:820px;padding-top:28px">' + backBtn() +
        '<h1 class="q" tabindex="-1" style="margin-top:22px">' + esc(t('apH')) + '</h1>' +
        '<div class="notice">' + ICON.cal + '<span>' + t('apN') + '</span></div>' +
        '<div class="cal"><div><div class="mhead"><button type="button" class="nav" data-act="mon" data-v="-1" aria-label="Previous month"' + (S.month <= 0 ? ' disabled' : '') + '>‹</button><b aria-live="polite">' + esc(t('months')[mo] + ' ' + y) + '</b><button type="button" class="nav" data-act="mon" data-v="1" aria-label="Next month"' + (S.month >= 1 ? ' disabled' : '') + '>›</button></div>' +
        '<div class="grid">' + cells + '</div><p class="tz">' + esc(t('tz')) + '</p></div><div class="slots">' + slots + '</div></div>' +
        '<div class="actions"><button type="button" class="btn" data-act="book"' + (S.d.slot ? '' : ' disabled') + '>' + esc(t('book')) + ' ' + ICON.arrow + '</button></div></main>';
    }
    function vDone(){
      var d = S.d, p = d.day.split('-'), sd = new Date(+p[0], +p[1] - 1, +p[2]);
      var when = t('days')[sd.getDay()] + ', ' + sd.getDate() + ' ' + t('months')[sd.getMonth()] + ' ' + sd.getFullYear() + ' · ' + d.slot;
      return header() + '<main class="wrap" style="padding-top:36px">' +
        '<span class="ok-mark" aria-hidden="true">' + ICON.big + '</span>' +
        '<h1 class="q" tabindex="-1" style="margin-top:18px">' + esc(t('doneH')) + '</h1><p class="sub">' + esc(t('doneS')) + '</p>' +
        '<div class="sum"><div class="row"><span>' + esc(t('sPatient')) + '</span><b>' + esc(d.name.trim()) + (d.age !== '' ? ', ' + esc(d.age) : '') + '</b></div>' +
        '<div class="row"><span>' + esc(t('sWhen')) + '</span><b>' + esc(when) + '</b></div>' +
        '<div class="row"><span>' + esc(t('sCall')) + '</span><b>' + esc(d.meet ? t('meet') : t('wa') + ' · ' + d.cc + ' ' + d.phone) + '</b></div>' +
        '<div class="row" style="border-bottom:0"><span>' + esc(t('sLang')) + '</span><b>' + (d.mail === 'tr' ? 'Türkçe' : 'English') + '</b></div></div>' +
        '<div class="notice go">' + ICON.chat + '<span>' + t('now') + '</span></div>' +
        '<div class="actions" style="margin-top:14px"><button type="button" class="btn ghost" data-act="wa">' + esc(t('msg')) + '</button></div>' +
        '<p class="sub" style="margin-top:22px">' + esc(t('send')) + '</p><div class="chips">' + t('recs').map(function(r){ return '<span>' + esc(r) + '</span>'; }).join('') + '</div>' +
        '<div class="tips"><h3>' + esc(t('prepH')) + '</h3><ul><li>' + esc(t('prep1')) + '</li><li>' + esc(d.meet ? t('prep2meet') : t('prep2wa')) + '</li></ul></div>' +
        '<p class="alt" style="text-align:left">' + esc(t('contact')) + ' <b>' + PHONE + '</b></p>' +
        '<div class="sandbox"><span>Portfolio copy: nothing was sent, paid or booked.</span><button type="button" class="btn ghost" data-act="restart" style="min-height:38px;padding:0 16px">Start again</button></div></main>';
    }

    function render(focus){
      var html = S.screen === 'intro' ? vIntro() : S.screen === 'q' ? vQ() : S.screen === 'pay' ? vPay() : S.screen === 'lang' ? vLang() : S.screen === 'appt' ? vAppt() : vDone();
      app.innerHTML = html;
      dlgSlot.innerHTML = S.dlg ? vDlg() : '';
      if(S.dlg){ var y = dlgSlot.querySelector('[data-act="dlg-yes"]'); if(y) y.focus(); return; }
      if(focus){
        app.scrollTop = 0;
        var f = app.querySelector('#f');
        if(f && S.screen === 'q'){ focusEnd(f); }
        else { var h = app.querySelector('h1'); if(h) h.focus({preventScroll:true}); }
      }
    }
    function focusEnd(f){
      f.focus({preventScroll:true});
      if(f.setSelectionRange && (f.tagName === 'TEXTAREA' || f.type === 'text' || f.type === 'tel')){ try{ var L = f.value.length; f.setSelectionRange(L, L); }catch(e){} }
    }
    function go(screen, q){ S.screen = screen; if(q != null) S.q = q; S.err = ''; render(true); }

    function validate(){
      var d = S.d;
      if(S.screen === 'q'){
        if(S.q === 0 && d.name.trim().split(/\s+/).filter(Boolean).length < 2) return t('q1e');
        if(S.q === 1){ var a = d.age === '' ? NaN : Number(d.age); if(!(a >= 0 && a <= 120) || String(d.age).indexOf('.') > -1) return t('q2e'); }
        if(S.q === 2 && !d.meet && d.phone.replace(/\D/g, '').length < 7) return t('q3e');
        if(S.q === 3 && !d.reasons.length) return t('q4e');
        if(S.q === 4 && d.surgery === null) return t('q5e');
      }
      if(S.screen === 'lang' && !d.mail) return S.lang === 'tr' ? 'Lütfen bir dil seçin' : 'Please choose a language';
      return '';
    }
    function next(){
      var e = validate();
      if(e){ S.err = e; render(false); var f = app.querySelector('#f') || app.querySelector('[role="group"] button'); if(f) focusEnd(f); return; }
      if(S.screen === 'q'){ if(S.q < 5) go('q', S.q + 1); else go('pay'); }
      else if(S.screen === 'lang') go('appt');
    }
    function back(){
      if(S.screen === 'q'){ if(S.q > 0) go('q', S.q - 1); else go('intro'); }
      else if(S.screen === 'pay') go('q', 5);
      else if(S.screen === 'lang') go('pay');
      else if(S.screen === 'appt') go('lang');
    }

    sr.addEventListener('click', function(e){
      var el = e.target.closest ? e.target.closest('[data-act]') : null; if(!el || !sr.contains(el)) return;
      var a = el.getAttribute('data-act'), v = el.getAttribute('data-v');
      if(a === 'lang'){ S.lang = v; S.err = ''; render(false); return; }
      if(a === 'home'){ go('intro'); return; }
      if(a === 'start'){ go('q', 0); return; }
      if(a === 'back'){ back(); return; }
      if(a === 'next'){ next(); return; }
      if(a === 'reason'){ var k = +v, r = S.d.reasons, ix = r.indexOf(k); if(ix > -1) r.splice(ix, 1); else r.push(k); S.err = ''; render(false); var b = app.querySelector('[data-act="reason"][data-v="' + k + '"]'); if(b) b.focus(); return; }
      if(a === 'yn'){ S.d.surgery = v === '1'; S.err = ''; render(false); setTimeout(function(){ if(S.screen === 'q' && S.q === 4) go('q', 5); }, 260); return; }
      if(a === 'paid'){ S.dlg = true; render(false); return; }
      if(a === 'dlg-no'){ S.dlg = false; render(false); var p = app.querySelector('[data-act="paid"]'); if(p) p.focus(); return; }
      if(a === 'dlg-yes'){ S.dlg = false; go('lang'); return; }
      if(a === 'copy'){ toast(S.lang === 'tr' ? 'Bu portfolyo kopyasında IBAN gizlidir.' : 'The IBAN is masked in this portfolio copy, so there\'s nothing to copy.'); return; }
      if(a === 'mail'){ S.d.mail = v; S.err = ''; render(false); var m = app.querySelector('[data-act="mail"][data-v="' + v + '"]'); if(m) m.focus(); return; }
      if(a === 'mon'){ S.month = Math.max(0, Math.min(1, S.month + (+v))); render(false); var n = app.querySelector('[data-act="mon"]:not([disabled])'); if(n) n.focus(); return; }
      if(a === 'day'){ S.d.day = v; S.d.slot = null; render(false); var dy = app.querySelector('[data-act="day"][data-v="' + v + '"]'); if(dy) dy.focus(); return; }
      if(a === 'slot'){ S.d.slot = v; render(false); var s = app.querySelector('[data-act="slot"][data-v="' + v + '"]'); if(s) s.focus(); return; }
      if(a === 'book'){ if(S.d.slot) go('done'); return; }
      if(a === 'wa'){ toast('On the live site this opens WhatsApp, with the message already written.'); return; }
      if(a === 'restart'){ fresh(); render(true); return; }
    });
    sr.addEventListener('input', function(e){
      var id = e.target.id, d = S.d;
      if(id === 'f'){
        if(S.q === 0) d.name = e.target.value;
        else if(S.q === 1) d.age = e.target.value;
        else if(S.q === 2) d.phone = e.target.value.replace(/[^\d\s()-]/g, '');
        else if(S.q === 5){ d.desc = e.target.value.slice(0, 500); var n = app.querySelector('#n'); if(n) n.textContent = d.desc.length; }
        if(S.err){ S.err = ''; var er = app.querySelector('.err'); if(er) er.remove(); e.target.classList.remove('bad'); e.target.setAttribute('aria-invalid', 'false'); }
      }
    });
    sr.addEventListener('change', function(e){
      if(e.target.id === 'cc') S.d.cc = e.target.value;
      if(e.target.id === 'meet'){ S.d.meet = e.target.checked; if(S.err){ S.err = ''; render(false); app.querySelector('#meet').focus(); } }
    });
    sr.addEventListener('keydown', function(e){
      if(S.dlg){
        if(e.key === 'Escape'){ e.preventDefault(); S.dlg = false; render(false); var p = app.querySelector('[data-act="paid"]'); if(p) p.focus(); }
        if(e.key === 'Tab'){ var bs = dlgSlot.querySelectorAll('button'); if(bs.length){ var f0 = bs[0], f1 = bs[bs.length - 1], act = sr.activeElement; if(e.shiftKey && act === f0){ e.preventDefault(); f1.focus(); } else if(!e.shiftKey && act === f1){ e.preventDefault(); f0.focus(); } } }
        return;
      }
      if(e.metaKey || e.altKey) return;
      var tag = e.target.tagName, typing = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
      if(S.screen === 'q'){
        if(e.key === 'Enter' && !e.shiftKey){
          if(tag === 'TEXTAREA' && !e.ctrlKey) return;
          var act = tag === 'BUTTON' ? e.target.getAttribute('data-act') : null;
          if(act && act !== 'next' && act !== 'reason') return;
          e.preventDefault(); next(); return;
        }
        if(typing || e.ctrlKey) return;
        var ch = (e.key || '').toLowerCase();
        if(S.q === 3 && /^[a-k]$/.test(ch)){ e.preventDefault(); var b = app.querySelector('[data-act="reason"][data-v="' + (ch.charCodeAt(0) - 97) + '"]'); if(b) b.click(); return; }
        if(S.q === 4 && (ch === t('ky') || ch === t('kn'))){ e.preventDefault(); var y = app.querySelector('[data-act="yn"][data-v="' + (ch === t('ky') ? 1 : 0) + '"]'); if(y) y.click(); return; }
      }
      if(S.screen === 'lang' && e.key === 'Enter' && e.target.getAttribute('data-act') !== 'mail' && !typing){ e.preventDefault(); next(); }
    });

    fresh(); render(false);
    return { restart: function(){ fresh(); render(true); } };
  }

  window.__protos = window.__protos || {};
  window.__protos.consultation = mount;
})();
