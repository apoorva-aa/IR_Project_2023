import React from 'react'

export default function Navbar() {
  return (
      <div className="navbar">
          <h1 class="text-4xl my-5 font-bold text-center text-slate-600">Lexical Text Simplification and Detoxification</h1>
          <div className="menu" class="bg-blue-500 overflow-hidden w-128 top-0">
              <div className="menu-items" class="text-2xl text-white" >
                  <a href="/" class="float-left text-center px-3 py-1 block hover:bg-gray-300 hover:text-black">Home</a>
                  <a href="aboutProject" class="float-left text-center px-3 py-1 block hover:bg-gray-300 hover:text-black">About Project</a>
                  <a href="team" class="float-left text-center px-3 py-1 block hover:bg-gray-300 hover:text-black">Team Members</a>
              </div>
          </div>
      </div>
  )
}
