import Feature05Domain
import Feature05Data

public enum Feature05PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature05DomainModel = Feature05DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
