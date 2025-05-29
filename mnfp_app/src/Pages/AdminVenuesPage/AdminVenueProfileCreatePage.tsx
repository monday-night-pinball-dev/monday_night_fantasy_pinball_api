import { MnfpEntityCreateProfile, ProfileCreateTemplate } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";
import {  useParams } from "react-router-dom";  
 
export const AdminVenueProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
   

  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([ 
      ['name', { title: 'Name' }],  
    ])
  
 
  return (
    <div>
      <MnfpEntityCreateProfile 
        entityId={id || ''} 
        entityApiName="venues" 
        entityNameSingular="Venue"  
        entityInboundCreateModelName="VenueInboundCreateModel"
        entityOutboundModelName="VenueOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}