import React from 'react'; 
const Footer = () => {
    return (
        <footer className="page-footer font-tiny text-light pt-4" style={{backgroundColor: '#3e4551'}}>
        <div className="container text-center text-md-left ">
        
        {/** Social Media Icons  **/}
            <ul className="list-unstyled list-inline text-center">
                <li className="list-inline-item mr-3">
                <h5 className="p-3 m-auto"> Reach out to us: </h5>
                </li>
                {/* Discord Invite */}
                <li className="list-inline-item mr-3">
                <a href="https://discord.gg/gj48prMv">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="#738adb" className="bi bi-discord" viewBox="0 0 16 16">
                    <path d="M6.552 6.712c-.456 0-.816.4-.816.888s.368.888.816.888c.456 0 .816-.4.816-.888.008-.488-.36-.888-.816-.888zm2.92 0c-.456 0-.816.4-.816.888s.368.888.816.888c.456 0 .816-.4.816-.888s-.36-.888-.816-.888z"/>
                    <path d="M13.36 0H2.64C1.736 0 1 .736 1 1.648v10.816c0 .912.736 1.648 1.64 1.648h9.072l-.424-1.48 1.024.952.968.896L15 16V1.648C15 .736 14.264 0 13.36 0zm-3.088 10.448s-.288-.344-.528-.648c1.048-.296 1.448-.952 1.448-.952-.328.216-.64.368-.92.472-.4.168-.784.28-1.16.344a5.604 5.604 0 0 1-2.072-.008 6.716 6.716 0 0 1-1.176-.344 4.688 4.688 0 0 1-.584-.272c-.024-.016-.048-.024-.072-.04-.016-.008-.024-.016-.032-.024-.144-.08-.224-.136-.224-.136s.384.64 1.4.944c-.24.304-.536.664-.536.664-1.768-.056-2.44-1.216-2.44-1.216 0-2.576 1.152-4.664 1.152-4.664 1.152-.864 2.248-.84 2.248-.84l.08.096c-1.44.416-2.104 1.048-2.104 1.048s.176-.096.472-.232c.856-.376 1.536-.48 1.816-.504.048-.008.088-.016.136-.016a6.521 6.521 0 0 1 4.024.752s-.632-.6-1.992-1.016l.112-.128s1.096-.024 2.248.84c0 0 1.152 2.088 1.152 4.664 0 0-.68 1.16-2.448 1.216z"/>
                </svg>
                </a>
                </li>

                {/* Github Repo */}
                <li className="list-inline-item mr-3">
                <a href="https://github.com/guyLee687/Recommendation-app-" style={{ color: '#FFF' }}>
                <svg xmlns="http://www.w3.org/2000/svg" href="https://github.com/guyLee687/Recommendation-app-" width="30" height="30" fill="currentColor" className="bi bi-github" viewBox="0 0 16 16">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                </svg></a>   
                </li>
                {/* Youtube channel (demos ) */}
                <li className="list-inline-item mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="rgba(255,0,0, 1)" className="bi bi-youtube" viewBox="0 0 16 16">
                    <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
                </svg>
                </li>
                {/* Email embed to maitto: (need project email) */}
                <li className="list-inline-item mr-3 ">
                <svg enableBackground="new 0 0 24 24" id="Layer_1" vidth="30" height ="30" version="1.1" viewBox="0 0 24 24" xmlSpace="preserve" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink"><g><path d="M12,5c1.6167603,0,3.1012573,0.5535278,4.2863159,1.4740601l3.637146-3.4699707   C17.8087769,1.1399536,15.0406494,0,12,0C7.392395,0,3.3966675,2.5999146,1.3858032,6.4098511l4.0444336,3.1929321   C6.4099731,6.9193726,8.977478,5,12,5z" fill="#F44336" /><path d="M23.8960571,13.5018311C23.9585571,13.0101929,24,12.508667,24,12   c0-0.8578491-0.093689-1.6931763-0.2647705-2.5H12v5h6.4862061c-0.5247192,1.3637695-1.4589844,2.5177612-2.6481934,3.319458   l4.0594482,3.204834C22.0493774,19.135437,23.5219727,16.4903564,23.8960571,13.5018311z" fill="#2196F3" /><path d="M5,12c0-0.8434448,0.1568604-1.6483765,0.4302368-2.3972168L1.3858032,6.4098511   C0.5043335,8.0800171,0,9.9801636,0,12c0,1.9972534,0.4950562,3.8763428,1.3582153,5.532959l4.0495605-3.1970215   C5.1484375,13.6044312,5,12.8204346,5,12z" fill="#FFC107" /><path d="M12,19c-3.0455322,0-5.6295776-1.9484863-6.5922241-4.6640625L1.3582153,17.532959   C3.3592529,21.3734741,7.369812,24,12,24c3.027771,0,5.7887573-1.1248169,7.8974609-2.975708l-4.0594482-3.204834   C14.7412109,18.5588989,13.4284058,19,12,19z" fill="#00B060" /><path d="M12,23.75c-3.5316772,0-6.7072754-1.4571533-8.9524536-3.7786865C5.2453613,22.4378052,8.4364624,24,12,24   c3.5305786,0,6.6952515-1.5313721,8.8881226-3.9592285C18.6495972,22.324646,15.4981079,23.75,12,23.75z" opacity="0.1" /><polygon opacity="0.1" points="12,14.25 12,14.5 18.4862061,14.5 18.587492,14.25  " /><path d="M23.9944458,12.1470337C23.9952393,12.0977783,24,12.0493774,24,12   c0-0.0139771-0.0021973-0.0274658-0.0022583-0.0414429C23.9970703,12.0215454,23.9938965,12.0838013,23.9944458,12.1470337z" fill="#E6E6E6" /><path d="M12,9.5v0.25h11.7855721c-0.0157471-0.0825195-0.0329475-0.1680908-0.0503426-0.25H12z" fill="#FFFFFF" opacity="0.2" /><linearGradient gradientUnits="userSpaceOnUse" id="SVGID_1_" x1={0} x2={24} y1={12} y2={12}><stop offset={0} style={{stopColor: '#FFFFFF', stopOpacity: '0.2'}} /><stop offset={1} style={{stopColor: '#FFFFFF', stopOpacity: 0}} /></linearGradient><path d="M23.7352295,9.5H12v5h6.4862061C17.4775391,17.121582,14.9771729,19,12,19   c-3.8659668,0-7-3.1340332-7-7c0-3.8660278,3.1340332-7,7-7c1.4018555,0,2.6939087,0.4306641,3.7885132,1.140686   c0.1675415,0.1088867,0.3403931,0.2111206,0.4978027,0.333374l3.637146-3.4699707L19.8414307,2.940979   C17.7369385,1.1170654,15.00354,0,12,0C5.3725586,0,0,5.3725586,0,12c0,6.6273804,5.3725586,12,12,12   c6.1176758,0,11.1554565-4.5812378,11.8960571-10.4981689C23.9585571,13.0101929,24,12.508667,24,12   C24,11.1421509,23.906311,10.3068237,23.7352295,9.5z" fill="url(#SVGID_1_)" /><path d="M15.7885132,5.890686C14.6939087,5.1806641,13.4018555,4.75,12,4.75c-3.8659668,0-7,3.1339722-7,7   c0,0.0421753,0.0005674,0.0751343,0.0012999,0.1171875C5.0687437,8.0595093,8.1762085,5,12,5   c1.4018555,0,2.6939087,0.4306641,3.7885132,1.140686c0.1675415,0.1088867,0.3403931,0.2111206,0.4978027,0.333374   l3.637146-3.4699707l-3.637146,3.2199707C16.1289062,6.1018066,15.9560547,5.9995728,15.7885132,5.890686z" opacity="0.1" /><path d="M12,0.25c2.9750366,0,5.6829224,1.0983887,7.7792969,2.8916016l0.144165-0.1375122   l-0.110014-0.0958166C17.7089558,1.0843592,15.00354,0,12,0C5.3725586,0,0,5.3725586,0,12   c0,0.0421753,0.0058594,0.0828857,0.0062866,0.125C0.0740356,5.5558472,5.4147339,0.25,12,0.25z" fill="#FFFFFF" opacity="0.2" /></g><g /><g /><g /><g /><g /><g /><g /><g /><g /><g /><g /><g /><g /><g /><g /></svg>
                </li>
            </ul>
            <div className="row">
            <div className="col-md-5 mx-auto">
                <h6 className="font-weight-bold  mt-3 mb-4">RecoSummary</h6>
                <p>Get started with RecomMedia today, and gain access to personalized
                recommendation lists based the things you love.
                adipisicing elit.</p>
            </div>
            <hr className="clearfix w-100 d-md-none" />
            <div className="col-md-2 mx-auto">
                <h6 className="font-weight-bold text-uppercase mt-3 mb-4">Site Links</h6>
                <ul className="list-unstyled">
                <li>
                    <a href="#!">About Us</a>
                </li>
                <li>
                    <a href="#!">Contact Us</a>
                </li>
                <li>
                    <a href="#!">FAQ</a>
                </li>
                </ul>
            </div>
            <hr className="clearfix w-100 d-md-none" />
            <div className="col-md-2 mx-auto">
                <h6 className="font-weight-bold text-uppercase mt-3 mb-4"> User </h6>
                <ul className="list-unstyled">
                <li>
                    <a href="/user/profile">Profile </a>
                </li>
                <li>
                    <a href="/list">Movie List</a>
                </li>
                </ul>
            </div>
            <hr className="clearfix w-100 d-md-none" />
            <div className="col-md-2 mx-auto">
                <h6 className="font-weight-bold text-uppercase mt-3 mb-4">Media Sites</h6>
                <ul className="list-unstyled">
                <li>
                    <a href="https://www.imdb.com/">IMDB</a>
                </li>
                <li>
                    <a href="https://myanimelist.net/">MyAnimeList</a>
                </li>
                <li>
                    <a href="https://www.goodreads.com/">GoodReads</a>
                </li>
                <li>
                    <a href="https://comicbookroundup.com/">Comic Book RoundUp</a>
                </li>
                </ul>
            </div>
            </div>
        </div>
        <hr />
        <ul className="list-unstyled list-inline text-center py-2">
            <li className="list-inline-item">
            <h5 className="mb-1">Register Here: </h5>
            </li>
            <li className="list-inline-item">
            <a href="#!" className="btn btn-danger btn-rounded">Sign up!</a>
            </li>
        </ul>
        <hr />
        <div className="footer-copyright text-center py-3" style={{backgroundColor: "rgba(0,0,0,2)"}}>© 2020 Copyright:
            <a href="https://mdbootstrap.com/"> MDBootstrap.com</a>
        </div>
        </footer>

    );
}

export default Footer


