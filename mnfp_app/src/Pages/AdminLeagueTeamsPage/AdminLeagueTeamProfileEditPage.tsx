import {  useParams } from "react-router-dom"; 
import {  ProfileFieldEditTypes } from "@/Components/EntityProfileComponents/MnfpEntityProfile";
import { MnfpEntityEditProfile, ProfileEditTemplate } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";

     
 
export const AdminLeagueTeamProfileEditPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileEditTemplate = new  ProfileEditTemplate([ 
    ['name', { title: 'Name' }],
    ['short_name', { title: 'Short Name' }], 
    ['home_venue_id', {
        title: 'Venue', 
        typeOverride: {
          type: ProfileFieldEditTypes.FK_LINK,
          typeParams: {
            optionNameKey: 'name',
            searchKey: 'name_like',
            searchUrl: '/venues',
          } 
        } 
      }],
    ['global_mnp_id', { title: 'MNP ID' }],
    ['created_at', { title: 'Created At' }], 
  ]);
   
  return (
    <div>
      <MnfpEntityEditProfile 
        entityId={id || ''} 
        entityApiName="league_teams" 
        entityNameSingular="League Team"  
        entityInboundUpdateModelName="LeagueTeamInboundUpdateModel"
        entityOutboundModelName="LeagueTeamOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}