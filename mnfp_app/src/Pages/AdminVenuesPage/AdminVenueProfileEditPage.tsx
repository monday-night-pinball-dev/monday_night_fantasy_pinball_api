import {  useParams } from "react-router-dom"; 
import { MnfpEntityEditProfile, ProfileEditTemplate } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";
 
export const AdminVenueProfileEditPage : React.FC = () => {
      
  const { id } = useParams();  
   

  const profileTemplate: ProfileEditTemplate = new ProfileEditTemplate([ 
      ['name', { title: 'Name' }], 
      ['created_at', { title: 'Created At' }], 
    ])
  
 
  return (
    <div>
      <MnfpEntityEditProfile 
        entityId={id || ''} 
        entityApiName="venues" 
        entityNameSingular="Venue"  
        entityInboundUpdateModelName="VenueInboundUpdateModel"
        entityOutboundModelName="VenueOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}