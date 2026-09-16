import Feature20Domain
import Feature20Data

public enum Feature20PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature20DomainModel = Feature20DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
