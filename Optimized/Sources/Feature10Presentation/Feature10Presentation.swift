import Feature10Domain
import Feature10Data

public enum Feature10PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature10DomainModel = Feature10DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
