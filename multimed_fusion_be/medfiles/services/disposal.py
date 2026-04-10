from django.utils import timezone

from medfiles.models import PatientDocChunk, PatientFile
from portal.models import PatientDoctorAccess


def dispose_file(file_obj, *, reason: str) -> None:
    if file_obj.is_disposed:
        return

    file_obj.is_disposed = True
    file_obj.disposed_at = timezone.now()
    file_obj.processing_status = "disposed"
    file_obj.last_error = reason
    if file_obj.file:
        file_obj.file.delete(save=False)
    file_obj.save()
    PatientDocChunk.objects.filter(
        patient=file_obj.patient,
        doctor=file_obj.doctor,
        source_file_ids__contains=[str(file_obj.id)],
    ).delete()


def dispose_expired_files(*, now=None) -> int:
    now = now or timezone.now()
    count = 0
    for file_obj in PatientFile.objects.filter(is_disposed=False):
        expired = bool(file_obj.authorized_until and file_obj.authorized_until <= now)
        link_revoked = PatientDoctorAccess.objects.filter(
            doctor=file_obj.doctor,
            patient=file_obj.patient,
            status=PatientDoctorAccess.Status.REVOKED,
        ).exists()
        if expired or link_revoked:
            dispose_file(file_obj, reason="Authorization expired or revoked")
            count += 1
    return count
