import React from 'react';
import {Jumbotron, Container} from 'react-bootstrap'
import Image from '../pics/wp1841194-santa-cruz-california-wallpapers.jpg';
import styled from 'styled-components';

const Styles = styled.div`
    .jumbo{
        background: url(${Image}) no-repeat fixed bottom;
        background-size: cover;
        background-color: transparent;
        color: transparent;
        height: 600px;
        position: relative;
        z-index: 0;
    }

    .overlay{
        background-color: transparent;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        z-index: -1;
    }

    .title{
        margin-top: 75px;
        font-size: xxx-large;
        background-color: rgba(0, 0, 0, .35) !important;
        color: white !important;
        text-align: center;
    }

    .contain {
        background-color: rgba(0, 0, 0, 0.0) !important;
    }

    .desc {
        margin-top: 75px;
        color: white !important;
        background-color: rgba(0, 0, 0, .35) !important;
        text-align: center;
    }
`

function HpHeader(){
    return(
        <Styles>
            <Jumbotron fluid className = "jumbo">
                <div className = "overlay"></div>
                <Container className = "contain">
                    <h1 className = "title">
                        Tired of garbage media recommendations?
                    </h1>
                    <p className = "desc">
                        Get started with RecomMedia today, and gain access to personalized
                        recommendation lists based the things you love.
                    </p>
                    <p className = "desc">
                        Scroll down to view a complete list of media.
                    </p>
                </Container>
            </Jumbotron>
        </Styles>
    )
}

export default HpHeader;
