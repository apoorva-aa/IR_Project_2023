import React from 'react'
import Navbar from './Navbar'
export default function Team() {
  return (
    <div>
      
      <Navbar />
      <div className="teamContainer flex flex-wrap justify-center items-center">
        
        <div className="teamMember flex flex-col justify-center items-center m-8">
          <img className = "h-64"src="https://avatars.githubusercontent.com/u/54908789?v=4" alt="team member" />
          <h1 className="text-lg font-serif my-2">Aniket Goel</h1>
        </div>
        <div className="teamMember flex flex-col justify-center items-center m-8">
          <img className = "h-64"src="https://avatars.githubusercontent.com/u/54908789?v=4" alt="team member" />
          <h1 className="text-lg font-serif my-2">Abhimanyu Bhatnagar</h1>
        </div>
        <div className="teamMember flex flex-col justify-center items-center m-8">
          <img className = "h-64"src="https://avatars.githubusercontent.com/u/54908789?v=4" alt="team member" />
          <h1 className="text-lg font-serif my-2">Apoorva Arya</h1>
        </div>
        <div className="teamMember flex flex-col justify-center items-center m-8">
          <img className = "h-64"src="https://avatars.githubusercontent.com/u/54908789?v=4" alt="team member" />
          <h1 className="text-lg font-serif my-2">Aanya Trehan</h1>
        </div>
        <div className="teamMember flex flex-col justify-center items-center m-8">
          <img className = "h-64"src="https://avatars.githubusercontent.com/u/54908789?v=4" alt="team member" />
          <h1 className="text-lg font-serif my-2">Sejal Kardam</h1>
        </div>
        <div className="teamMember flex flex-col justify-center items-center m-8">
          <img className = "h-64"src="https://avatars.githubusercontent.com/u/54908789?v=4" alt="team member" />
          <h1 className="text-lg font-serif my-2">Naman Kaushik</h1>
        </div>
        
      </div>
      
    </div>
  )
}
