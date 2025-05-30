import {  useParams } from "react-router-dom"; 
import { MnfpEntityReadProfile, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";
     

export const AdminSeasonProfileReadPage : React.FC = () => {
     
  const { id } = useParams();  
   

  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['name', { title: 'Name' }],
      ['season_number', { title: 'Season Number' }],
      ['created_at', { title: 'Created At' }], 
    ])
  
  return (
    <div>
      <MnfpEntityReadProfile 
        entityId={id || ''} 
        entityApiName="seasons" 
        entityNameSingular="Season"  
        entityOutboundModelName="SeasonOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}