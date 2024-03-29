import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
function HomePage() {
    const [text, setText] = useState('');
    const [result, setResult] = useState('Your result will appear here ');
    const sendRequest = async () => {
        setResult('Loading...');
        await axios
            .post('http://127.0.0.1:5000/getResult', {
                textToSimplify: text,

            })
            .then((res) => {

                setResult("Simplified: " + res.data);
            })
            .catch((err) => {
                console.log(err.message);
            });
    }
    const sendRequest2 = async () => {
        setResult('Loading...');
        await axios
            .post('http://127.0.0.1:5000/getDResult', {
                textToDetoxify: text,

            })
            .then((res) => {

                setResult("Detoxified: " + res.data);
            })
            .catch((err) => {
                console.log(err.message);
            });
    }
    const changeText = (e) => {
        setText(e.target.value);
    };
    return (
        <div>
            <Navbar />
            <div class="flex flex-col items-center my-4 ">
                <h1 class="text-4xl text-center text-gray-900">Instructions</h1>
                <ul class="list-disc">
                    <li className="text-xl text-gray-900">Enter the text to be simplified in the text box below.</li>
                    <li className="text-xl text-gray-900">Click on the Simplify Text button to get the simplified text.</li>
                    <li className="text-xl text-gray-900">Click on the Detoxify Text button to get the detoxified text.</li>
                    <li className="text-xl text-gray-900">Kindly enter appropriate punctuations for the model to understand context for better results</li>

                </ul>
                
               
            </div>
            <div className >
                <ul className="list-disc">
                   
                </ul>
            </div>
            <label class="relative block">
                <input class="mx-[10%] my-[2%] placeholder:italic placeholder:text-slate-400 block bg-white w-[70%] h-[40%] border border-slate-300 rounded-md py-2 pl-9 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm" placeholder="Enter the text to be simplified..." type="text" name="search" onChange={changeText} />
            </label>
            <div className="flex flex-col items-center">
                <button class="mx-10 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={sendRequest}>Simplify Text</button>
                <button class="mx-10 my-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={sendRequest2}>Detoxify Text</button>
            </div>
            <div class="mx-20 flex flex-col items-center">{`${result}`}</div>
        </div>
    );
}
export default HomePage;