
import {  useEffect, useState } from "react";
import {  useParams } from "react-router-dom"; 
import { MnfpProfilePage, ProfileFieldCreateTypes, ProfileFieldEditTypes, ProfileFieldReadTypes, ProfileModes, ProfileTemplate, ProfileTemplateCreateItem, ProfileTemplateEditItem, ProfileTemplateReadItem } from "@/Components/EntityProfileComponents/MnfpEntityProfile";

     
export const combineUniqueArrays = (...arrays: any) => {
  const combinedArray = [].concat(...arrays);
  return [...new Set(combinedArray)];
}

type AdminLeagueTeamProfilePageProps = {
  mode?: ProfileModes;
}

export const AdminLeagueTeamProfilePage : React.FC<AdminLeagueTeamProfilePageProps> = ({mode}) => {
     
  const [profileMode, setProfileMode] = useState<ProfileModes>(ProfileModes.READ);
  const { id } = useParams();  
     
  const profileTemplate: ProfileTemplate = {
     readTemplate: new Map<string, ProfileTemplateReadItem>([
      ['name', { title: 'Name' }],
      ['short_name', { title: 'Short Name' }],
      ['global_mnp_id', { title: 'MNP ID' }],
      ['home_venue_id', {
         title: 'Venue', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'home_venue_id',
              profileUrl: '/admin/venues',
            } 
          } 
        }],
      ['created_at', { title: 'Created At' }], 
    ]),
    createTemplate: new Map<string, ProfileTemplateCreateItem>([  
      ['name', { title: 'Name' }],
      ['short_name', { title: 'Short Name' }],
      ['global_mnp_id', { title: 'MNP ID' }],
      ['home_venue_id', {
         title: 'Venue', 
         typeOverride: {
            type: ProfileFieldCreateTypes.FK_LINK, 
          } 
        }],
    ]),
    editTemplate: new Map<string, ProfileTemplateEditItem>([
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
    ]),
  }

  useEffect(() => {
    if(mode) {
      setProfileMode(mode);
    } 
  }, [])
  
  return (
    <div>
      <MnfpProfilePage 
        entityId={id || ''} 
        entityNamePlural="league_teams"
        entityNameSingular="LeagueTeam" 
        entityInboundCreateModelName="LeagueTeamInboundCreateModel"
        entityInboundUpdateModelName="LeagueTeamInboundUpdateModel"
        entityOutboundModelName="LeagueTeamOutboundModel"
        mode={profileMode}
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}